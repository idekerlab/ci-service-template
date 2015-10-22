package org.cytoscape.ci;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

public class ConfigReader {

	// Number of instances for this type of worker
	private static final String NUM_INSTANCES = "instances";

	private final ObjectMapper mapper;
	private final WorkerBuilder builder;
	
	public ConfigReader() {
		this.mapper = new ObjectMapper(new YAMLFactory());
		this.builder = new WorkerBuilder();
	}
	
	public Collection<BaseWorker> read(final URL fileLocation) throws JsonParseException, JsonMappingException, IOException {
		
		final Map<String, ?> config = mapper.readValue(fileLocation, Map.class);
		
		return config.values().stream()
			.flatMap(workerConfig -> buildWorkers(workerConfig).stream())
			.collect(Collectors.toList());
	}
	
	private final Collection<BaseWorker> buildWorkers(Object workerConfig) {
		if(workerConfig instanceof LinkedHashMap == false) {
			throw new IllegalArgumentException("Worker Configuration is not LinkedHashMap.");
		}
		
		@SuppressWarnings("rawtypes")
		final LinkedHashMap<String, ?> configMap = (LinkedHashMap) workerConfig;
		
		Integer numInstances = Integer.parseInt(configMap.get(NUM_INSTANCES).toString());
		
		final List<BaseWorker> workers = new ArrayList<>();
		for(int i=0; i<numInstances; i++) {
			try {
				workers.add(builder.build((LinkedHashMap<String, ?>) workerConfig));
			} catch (JsonProcessingException e) {
				e.printStackTrace();
			}
		}
		return workers;
	}
	
	public static class ExecUtil {
		public static void stop(ExecutorService executor) {
			try {
				executor.shutdown();
				executor.awaitTermination(Long.MAX_VALUE, TimeUnit.DAYS);
			} catch (Exception e) {
				e.printStackTrace();
				System.err.println("termination interrupted");
			} finally {
				if (!executor.isTerminated()) {
					System.err.println("killing non-finished tasks");
				}
				executor.shutdownNow();
			}
		}
	}

	public static void main(String[] args) {
		
		try {
			// parse the command line arguments
			final CommandLineParser parser = new DefaultParser();
			final Options options = new Options();
			options.addOption("c", "config", true, "Worker configuration file");

			// parse the command line arguments
			CommandLine line = parser.parse(options, args);

			final String configFileLocation = line.getOptionValue("c");
			
			final ConfigReader reader = new ConfigReader();
		
			final File f = new File(configFileLocation);
			final Collection<BaseWorker> workers = reader.read(f.toURI().toURL());
			
			final ExecutorService executor = Executors.newWorkStealingPool();
			
			workers.stream()
					.forEach(
							worker->executor.submit(new ListenTask(worker))
							);

			ExecUtil.stop(executor);
			
			
		} catch (Exception exp) {
			exp.printStackTrace();
			System.out.println("Unexpected exception:" + exp.getMessage());
		}
	}
	
	
	
	
}