package org.cytoscape.ci;

import java.util.logging.Logger;

public class ListenTask implements Runnable {

	private static final Logger logger = Logger.getLogger("listener");

	private final Worker worker;

	public ListenTask(final Worker worker) {
		this.worker = worker;
	}

	@Override
	public void run() {
		logger.info(worker.id + ": Listening...");
		worker.listen();
		logger.info(worker.id
				+ ": !!!!!!!!!!!!! Listener Interrupted !!!!!!!!!!!!!!!!");
	}
}
