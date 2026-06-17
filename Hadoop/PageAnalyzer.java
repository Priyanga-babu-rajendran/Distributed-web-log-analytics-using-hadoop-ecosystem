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

public class PageAnalyzer {

    public static class PageMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text pageKey = new Text();

        // Looks inside the quotes, skips GET/POST/HEAD, and captures the exact URL asset path
        private static final Pattern logPattern = Pattern.compile(
            "^\\S+.*?\"(?:GET|POST|HEAD)\\s+(\\S+)\\s+.*\""
        );

        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            Matcher matcher = logPattern.matcher(line);

            if (matcher.find()) {
                String resourcePath = matcher.group(1); // Group 1 captures the raw URL path
                if (resourcePath != null && !resourcePath.isEmpty() && resourcePath.length() < 250) {
                pageKey.set(resourcePath);
                context.write(pageKey, one);
            }
            }
        }
    }

    public static class PageReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
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

    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.err.println("Usage: PageAnalyzer <input path> <output path>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "NASA Most Accessed Web Resources Analysis");
        job.setJarByClass(PageAnalyzer.class);
        job.setMapperClass(PageMapper.class);
        job.setCombinerClass(PageReducer.class);
        job.setReducerClass(PageReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
