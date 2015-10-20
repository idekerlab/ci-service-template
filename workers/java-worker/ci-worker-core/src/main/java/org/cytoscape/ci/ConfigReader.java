package org.cytoscape.ci;

import java.io.IOException;
import java.net.URL;
import java.util.Map;

import org.cytoscape.ci.config.WorkerConfiguration;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

public class ConfigReader {
	
	private final ObjectMapper mapper;
	
	
	public ConfigReader() {
		this.mapper = new ObjectMapper(new YAMLFactory());
	}
	
	public Map<String, Worker> read(final URL fileLocation) throws JsonParseException, JsonMappingException, IOException {
		Map<String, Worker> workerConfig = mapper.readValue(fileLocation, Map.class);
		return workerConfig;
	}

}
