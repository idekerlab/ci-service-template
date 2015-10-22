package org.cytoscape.ci;

public interface Worker {

	/**
	 * Do actual computation and return result as serialized JSON.
	 * 
	 * @param rawData input data as serialized JSON (string)
	 * @return result in serialized JSON
	 * @throws Exception
	 */
	public String run(final String rawData) throws Exception;
	
	public void listen();
}
