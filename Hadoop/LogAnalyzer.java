import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class LogAnalyzer {

    // MAPPER CLASS
    public static class LogMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text outputKey = new Text();
        private String analysisType;

        @Override
        protected void setup(Context context) {
            // Get the user-selected analysis type from configuration
            analysisType = context.getConfiguration().get("analysis.type", "STATUS");
        }

        // Regex pattern to clean and parse standard Apache log lines reliably
               private static final Pattern logPattern = Pattern.compile(
            "^(\\S+).*?\"\\s*([0-9]{3})\\s.*"
        );

        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            Matcher matcher = logPattern.matcher(line);

            if (matcher.matches()) {
                String ipAddress = matcher.group(1); // Group 1: IP Address
                String statusCode = matcher.group(2); // Group 2: 3-Digit Status Code
                String pageResource = "/";            // Temporary placeholder to make compilation pass

                // Emit the correct key based on your methodology target
                if (analysisType.equalsIgnoreCase("IP")) {
                    outputKey.set(ipAddress);
                } else if (analysisType.equalsIgnoreCase("PAGE")) {
                    outputKey.set(pageResource);
                } else {
                    outputKey.set(statusCode); // Default to Status Code Analysis
                }
                context.write(outputKey, one);
            }
        }
    }

    // REDUCER CLASS
    public static class LogReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    // DRIVER LAYER
    public static void main(String[] args) throws Exception {
        if (args.length < 3) {
            System.err.println("Usage: LogAnalyzer <input path> <output path> <IP|PAGE|STATUS>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        // Pass the analysis selection string to the distributed cluster nodes
        conf.set("analysis.type", args[2]);

        Job job = Job.getInstance(conf, "NASA Log Analyzer: " + args[2]);
        job.setJarByClass(LogAnalyzer.class);
        job.setMapperClass(LogMapper.class);
        job.setCombinerClass(LogReducer.class); // Local aggregation optimize
        job.setReducerClass(LogReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
