package org.cytoscape.ci;

public interface Worker {

	/**
	 * 
	 * Do actual computation/processing and return the result as JSON
	 * 
	 * @param rawData input data as a serialized JSON string
	 * 
	 * @return result as a serialized JSON
	 * @throws Exception
	 */
	public String run(final String rawData) throws Exception;

	/**
	 * Start listening to messages via ZeroMQ
	 */
	public void listen();
}
