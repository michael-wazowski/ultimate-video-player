<script>
    import { writable } from "svelte/store";
	import { formatToMins } from "$lib/core/formatting";
    //import { Border, Grid } from "$lib/components"

	import ArcSlider from "./ArcSlider.svelte";

	// These values are bound to properties of the video
	let time = writable(0); //i cant remember why i changed this
	let duration;
	let paused = true;

	let showControls = true;
	let showControlsTimeout;

	export let fileSource = "";

    let thumbNailSource = fileSource+"/thumb";
	let subSource = fileSource+"/vtt"

	let captionTrack;

	// Used to track time of last mouse down event
	let lastMouseDown;

	function handleMove(e) {
		// Make the controls visible, but fade out after
		// 2.5 seconds of inactivity
		clearTimeout(showControlsTimeout);
		showControlsTimeout = setTimeout(() => (showControls = false), 2500);
		showControls = true;

		if (!duration) return; // video not loaded yet
		if (e.type !== 'touchmove' && !(e.buttons & 1)) return; // mouse not down

		const clientX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
		const { left, right } = this.getBoundingClientRect();
		$time = (duration * (clientX - left)) / (right - left);
	}

	// we can't rely on the built-in click event, because it fires
	// after a drag — we have to listen for clicks ourselves
	function handleMousedown(e) {
		lastMouseDown = new Date();
	}

	function handleMouseup(e) {
		if (new Date() - lastMouseDown < 300) {
			if (paused) e.target.play();
			else e.target.pause();
		}
	}

</script>

<div style="width: 70%; margin: 0 auto; margin-left: 5%">
	<video
		poster={thumbNailSource}
		src={fileSource}
		on:mousemove={handleMove}
		on:touchmove|preventDefault={handleMove}
		on:mousedown={handleMousedown}
		on:mouseup={handleMouseup}
		bind:currentTime={$time}
		bind:duration
		bind:paused
		crossorigin="anonymous"
		id="video"
	>
		<track kind="captions" id="captionTrack" default src={subSource} bind:this={captionTrack}/>
	</video>

	<div class="controls" style="opacity: {duration && showControls ? 1 : 0}">
		<progress value={$time / duration || 0} />

		<div class="info">
			<span class="time">{formatToMins($time)}</span>
			<span>click anywhere to {paused ? 'play' : 'pause'} / drag to seek</span>
			<span class="time">{formatToMins(duration)}</span>
		</div>
	</div>
	<ArcSlider bind:time={$time} captionTrack={captionTrack} duration={duration}/>
</div>

<style>
	div {
		position: relative;
	}

	.controls {
		position: absolute;
		top: 0;
		width: 100%;
		transition: opacity 1s;
	}

	.info {
		display: flex;
		width: 100%;
		justify-content: space-between;
	}

	span {
		padding: 0.2em 0.5em;
		color: white;
		text-shadow: 0 0 8px black;
		font-size: 1.4em;
		opacity: 0.7;
	}

	.time {
		width: 3em;
	}

	.time:last-child {
		text-align: right;
	}

	progress {
		display: block;
		width: 100%;
		height: 10px;
		-webkit-appearance: none;
		appearance: none;
	}

	progress::-webkit-progress-bar {
		background-color: rgba(0, 0, 0, 0.2);
	}

	progress::-webkit-progress-value {
		background-color: rgba(255, 255, 255, 0.6);
	}

	video {
		width: 100%;
	}
</style>
