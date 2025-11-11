<script>
	import { seo } from '$lib';
	import HeroSection from '$lib/components/landing/HeroSection.svelte';
	import SphereMask from '$lib/components/magic/SphereMask/SphereMask.svelte';
	import About from '$lib/components/landing/About.svelte';
	import Timer from '$lib/components/landing/Timer.svelte';
	import Prizes from '$lib/components/landing/Prizes.svelte';
	export let data;
</script>

<svelte:head>
	<title>{seo.title}</title>
	<meta name="description" content={seo.description} />
	<meta name="keywords" content={seo.keywords} />

	<meta property="og:title" content={seo.title} />
	<meta property="og:description" content={seo.description} />
	<meta property="og:image" content={seo.image} />
	<meta property="og:site_name" content={seo.title} />
	<meta property="og:url" content={seo.url} />

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={seo.title} />
	<meta name="twitter:description" content={seo.description} />
	<meta name="twitter:image" content={seo.image} />
	<meta name="twitter:site" content="@Tahmid Choudhury" />
</svelte:head>

<HeroSection />
<About />
<Prizes />
<Timer data={{ targetDate: data.targetDate }}/>
<SphereMask />