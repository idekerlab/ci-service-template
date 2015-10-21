package org.cytoscape.ci;

import static org.junit.Assert.*;

import java.io.File;
import java.net.URI;
import java.util.Collection;
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
		final ConfigReader reader = new ConfigReader();
		
		final Collection<Worker> workers = reader.read(getURI("config1.yml").toURL());
		int workerCount = workers.size();
		System.out.println(workerCount);
		assertEquals(5, workerCount);
	}
	
	private final URI getURI(final String fileName) throws Exception {
		final File f = new File("./src/test/resources/" + fileName);

		return f.toURI();
	}

}
