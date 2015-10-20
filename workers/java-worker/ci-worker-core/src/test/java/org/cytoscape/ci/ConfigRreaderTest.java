package org.cytoscape.ci;

import java.io.File;
import java.net.URI;
import java.util.Map;

import org.cytoscape.ci.config.WorkerConfiguration;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

public class ConfigRreaderTest {

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}

	@Test
	public void testRead() throws Exception {
		ConfigReader reader = new ConfigReader();
		
		Map<String, Worker> result = reader.read(getURI("config1.yml").toURL());
		System.out.println(result.keySet());
		
		Object worker = result.get("scalefree");
		System.out.println(result.keySet());
		ObjectMapper mapper = new ObjectMapper(new YAMLFactory());
		System.out.println(worker.toString());
		
	}
	
	private final URI getURI(final String fileName) throws Exception {
		final File f = new File("./src/test/resources/" + fileName);

		return f.toURI();
	}

}
