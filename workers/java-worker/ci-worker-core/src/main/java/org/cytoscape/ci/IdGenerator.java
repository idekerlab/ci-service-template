package org.cytoscape.ci;

import java.util.concurrent.atomic.AtomicLong;

public final class IdGenerator {
	
	private static final AtomicLong count = new AtomicLong(1);

	public static final Long getID() {
		return count.incrementAndGet();
	}

}
