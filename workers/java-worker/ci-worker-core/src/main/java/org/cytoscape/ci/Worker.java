package org.cytoscape.ci;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.zeromq.ZMQ;

public class Worker {

	private final ZMQ.Context context;
	
	private final ZMQ.Socket queue;
	private final ZMQ.Socket collector;
	private final ZMQ.Socket monitor;

	public Worker(final String serverIP, final Integer recieverPort,
			final Integer senderPort, final Integer monitorPort) {
		
		context = ZMQ.context(1);

		// Socket to receive messages on
		queue = context.socket(ZMQ.PULL);
		queue.connect("tcp://" + serverIP + ":" + recieverPort.toString());

		// Socket to send messages to
		collector = context.socket(ZMQ.PUSH);
		collector.connect("tcp://" + serverIP + ":" + senderPort.toString());

		// Socket to send messages to
		monitor = context.socket(ZMQ.PUSH);
		monitor.connect("tcp://" + serverIP + ":" + monitorPort.toString());
	}

	public void listen() {
		System.out.println("Java Worker: listening...");

		while (!Thread.currentThread().isInterrupted()) {
			String string = new String(queue.recv(0)).trim();
			long msec = Long.parseLong(string);
			// Simple progress indicator for the viewer
			System.out.flush();
			System.out.print(string + '.');

			// Send results to sink
			collector.send("".getBytes(), 0);
		}

		collector.close();
		queue.close();
		context.term();
	}

	public static void main(String[] args) {
		CommandLineParser parser = new DefaultParser();
		Options options = new Options();
		options.addOption("i", "server-ip", true, "Server IP Address");

		options.addOption("q", "queue-port", true, "Task queue port number");
		options.addOption("c", "collector-port", true, "Collector port number");
		options.addOption("m", "monitor-port", true, "Monitor port number");

		Worker worker = null;

		try {
			// parse the command line arguments
			CommandLine line = parser.parse(options, args);

			String serverIpAddress = "localhost";

			if (line.hasOption("i")) {
				serverIpAddress = line.getOptionValue("i");
			}
			final String queuePort = line.getOptionValue("q");
			final String collectorPort = line.getOptionValue("c");
			final String monitorPort = line.getOptionValue("m");

			worker = new Worker(serverIpAddress, Integer.parseInt(queuePort),
					Integer.parseInt(collectorPort),
					Integer.parseInt(monitorPort));

			worker.listen();

		} catch (ParseException exp) {
			System.out.println("Unexpected exception:" + exp.getMessage());
		}
	}
}
