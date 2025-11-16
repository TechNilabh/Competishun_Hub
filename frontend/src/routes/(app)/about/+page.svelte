<script lang="ts">
	import Sparkles from "$lib/components/ui/Sparkles.svelte";

	const config = {
    title: "National Talent Hackathon 2026",
    tagline:
      "A multi-stage national coding initiative led by the Department of Computer Science & Engineering, NIT Silchar — designed to assess clarity of thought, engineering discipline, and real-world AI/ML problem-solving.",
    registerLink: "/register",
    facts: [
      { label: "Organizer", value: "Dept. of CSE, NIT Silchar" },
      { label: "Team Size", value: "Up to 3 members" },
      { label: "Registration", value: "Till 30 Dec 2025" },
      { label: "Fee", value: "₹2000 / team" },
      { label: "Finale Venue", value: "NIT Silchar Campus (Offline)" }
    ],
    aboutInstitute:
      "Established in 1967 and declared an Institute of National Importance under the NIT Act 2007, NIT Silchar is recognized nationwide for engineering rigor, research depth, and academic distinction.",
    rankings: [
      { label: "NIRF Engineering 2024", value: "Rank 40" },
      { label: "NIRF Overall 2024", value: "Rank 92" },
      { label: "QS Asia 2025", value: "Rank 541" },
      { label: "Green Metric 2022", value: "Rank 205" }
    ],
    rounds: [
      {
        title: "Round 1 — Screening",
        when: "January 2026 (2nd week)",
        mode: "Online",
        details: "MCQs, aptitude evaluation, and foundational coding tasks."
      },
      {
        title: "Round 2 — AI/ML Coding",
        when: "February 2026 (1st week)",
        mode: "Online",
        details: "Coding challenges and focused AI/ML-driven problem statements."
      },
      {
        title: "Round 3 — Grand Finale",
        when: "February 2026 (last week)",
        mode: "Offline",
        details: "Real-time problem solving at NIT Silchar with curated test data."
      }
    ],
    prizes: [
      { place: "1st", amount: "₹50,000" },
      { place: "2nd", amount: "₹40,000" },
      { place: "3rd", amount: "₹30,000" }
    ],
    certificates: [
      "Participation Certificate",
      "Appreciation Certificate (≥50% or Top 75%)",
      "Outstanding Performance Certificate (Top 10%)"
    ],
    perks: [
      "Free accommodation during finale",
      "Campus & local exposure",
      "Faculty interactions & Gala Dinner"
    ],
    footerNote:
      "Account details and registration link will be provided by the organizers."
  };

	function onRegister() {
		window.location.href = config.registerLink;
	}
</script>

<section
	id="about"
	class="relative mx-auto max-w-6xl px-6 md:px-10 pt-36 pb-40 text-[var(--text-primary)] animate-fadeIn"
	role="main"
>

	<header class="relative mx-auto text-center">

		<h1
			id="hackathon-title"
			class="font-mono text-4xl md:text-6xl font-bold tracking-tight text-indigo-500 drop-shadow-sm"
		>
			{config.title}
		</h1>

		<p class="mt-6 text-lg md:text-xl text-[var(--text-secondary)] max-w-3xl mx-auto leading-8">
			{config.tagline}
		</p>

		<button
			on:click={onRegister}
			class="mt-10 font-mono text-sm px-7 py-3 border border-indigo-400
			       rounded-lg hover:bg-indigo-500 hover:text-white transition-all duration-300
			       shadow-sm hover:shadow-indigo-500/20"
		>
			Register Now
		</button>

		<!-- Sparkles Decoration -->
		<div class="relative h-40 w-full mt-24 pointer-events-none select-none">
			<div class="absolute inset-x-20 top-0 h-[2px] w-3/4 bg-indigo-500/40 blur-sm" />
			<div class="absolute inset-x-20 top-0 h-px w-3/4 bg-indigo-500/40" />
			<Sparkles
				minSize={0.8}
				maxSize={2}
				particleDensity={250}
				className="w-full h-full"
				particleColor="#9ca3af"
			/>
			<div
				class="absolute inset-0 bg-white dark:bg-black 
				       [mask-image:radial-gradient(350px_200px_at_top,transparent_25%,white)]"
			></div>
		</div>
	</header>

	<!-- Quick Facts Grid              -->
	<section class="mt-20 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-8" aria-label="Event facts">

		{#each config.facts as f}
			<div
				class="p-5 rounded-xl text-center border border-[var(--border)]
				       bg-[var(--card-bg)] shadow-lg shadow-black/10
				       hover:border-indigo-500 hover:shadow-indigo-500/20 transition-all cursor-default"
			>
				<p class="font-mono text-sm uppercase tracking-wide text-[var(--text-secondary)]">
					{f.label}
				</p>
				<p class="mt-3 text-xl text-indigo-500 font-bold">{f.value}</p>
			</div>
		{/each}

	</section>

	<!-- About NIT Silchar             -->
	<section class="mt-32 max-w-3xl mx-auto">
		<h2 class="font-mono text-2xl md:text-3xl font-semibold text-indigo-500 mb-6">
			About NIT Silchar
		</h2>

		<p class="text-[17px] leading-8 text-[var(--text-secondary)]">
			{config.aboutInstitute}
		</p>

		<ul class="mt-10 space-y-4">
			{#each config.rankings as r}
				<li
					class="flex justify-between text-[var(--text-primary)] font-mono text-sm
					       border-b border-[var(--border)] pb-3"
				>
					<span>{r.label}</span>
					<span class="text-indigo-500 font-semibold">{r.value}</span>
				</li>
			{/each}
		</ul>
	</section>

	<!-- Competition Structure          -->
	<section class="mt-32 max-w-3xl mx-auto">
		<h2 class="font-mono text-2xl md:text-3xl font-semibold text-indigo-500">
			Competition Structure
		</h2>

		<div class="mt-12 space-y-12">

			{#each config.rounds as r}
				<div
					class="p-6 rounded-xl bg-[var(--card-bg)] border border-[var(--border)]
					       shadow-lg shadow-black/10 hover:shadow-indigo-500/20
					       hover:border-indigo-500 transition-all"
				>
					<p class="font-mono text-base text-indigo-500 font-semibold">{r.title}</p>

					<p class="mt-3 flex gap-6 text-sm text-[var(--text-secondary)] font-mono opacity-80">
						<span>{r.mode}</span>
						<span>{r.when}</span>
					</p>

					<p class="mt-4 text-[16px] leading-7 text-[var(--text-primary)] opacity-90">
						{r.details}
					</p>
				</div>
			{/each}

		</div>
	</section>

	<!-- Prizes + Certificates          -->
	<section class="mt-32 grid md:grid-cols-2 gap-16 max-w-4xl mx-auto">

		<!-- Prizes -->
		<div>
			<h2 class="font-mono text-2xl md:text-3xl font-semibold text-indigo-500">Prizes</h2>

			<ul class="mt-10 space-y-6">
				{#each config.prizes as p}
					<li class="flex justify-between font-mono text-base border-b border-[var(--border)] pb-3">
						<span>{p.place}</span>
						<span class="text-indigo-500 font-semibold">{p.amount}</span>
					</li>
				{/each}
			</ul>
		</div>

		<!-- Certificates -->
		<div>
			<h2 class="font-mono text-2xl md:text-3xl font-semibold text-indigo-500">Certificates</h2>

			<ul class="mt-10 space-y-5 font-mono text-sm">
				{#each config.certificates as c}
					<li class="border-b border-[var(--border)] pb-2">{c}</li>
				{/each}
			</ul>
		</div>

	</section>

	<!-- Perks                         -->
	<section class="mt-32 max-w-3xl mx-auto">
		<h2 class="font-mono text-2xl md:text-3xl font-semibold text-indigo-500">
			What Participants Receive
		</h2>

		<ul class="mt-10 space-y-5 font-mono text-sm text-[var(--text-secondary)]">
			{#each config.perks as perk}
				<li>{perk}</li>
			{/each}
		</ul>
	</section>

</section>

<style>
	.animate-fadeIn {
		animation: fadeIn 0.5s ease-out;
	}

	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(20px); }
		to { opacity: 1; transform: translateY(0); }
	}
</style>
