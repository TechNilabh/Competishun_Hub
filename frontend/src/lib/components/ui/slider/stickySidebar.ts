export function stickySidebar(node: HTMLElement, options = { topSpacing: 20, bottomSpacing: 20 }) {
	let lastScroll = 0;

	function update() {
		const rect = node.getBoundingClientRect();
		const parent = node.parentElement!;
		const parentRect = parent.getBoundingClientRect();

		// Distance from top of the viewport
		const offsetTop = rect.top;

		// Bottom limit
		const parentBottom = parentRect.bottom - options.bottomSpacing - rect.height;

		if (parentRect.top < options.topSpacing && window.scrollY > lastScroll) {
			// Stick
			node.style.position = "fixed";
			node.style.top = `${options.topSpacing}px`;
			node.style.width = `${rect.width}px`;
		}

		// Stop sticking when hitting container bottom
		if (offsetTop >= parentBottom) {
			node.style.position = "absolute";
			node.style.top = `${parentBottom - parentRect.top}px`;
		}

		// Reset when above topSpacing
		if (parentRect.top >= options.topSpacing) {
			node.style.position = "relative";
			node.style.top = "0px";
			node.style.width = "auto";
		}

		lastScroll = window.scrollY;
	}

	window.addEventListener("scroll", update);
	window.addEventListener("resize", update);

	update();

	return {
		destroy() {
			window.removeEventListener("scroll", update);
			window.removeEventListener("resize", update);
		}
	};
}
