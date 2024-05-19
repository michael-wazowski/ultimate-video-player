<script>
    import { writable } from "svelte/store";
	import { formatToMins } from "$lib/core/formatting";
	import PlayIcon from "$lib/assets/play-icon.svg";
	import PauseIcon from "$lib/assets/pause-icon.svg";
	import FullscreenIcon from "$lib/assets/fullscreen-icon.svg";
	import FullscreenExitIcon from "$lib/assets/fullscreen-exit-icon.svg";
	import CaptionsIcon from "$lib/assets/captions-icon.svg";
	import CaptionsActiveIcon from "$lib/assets/captions-active-icon.svg";

    //import { Border, Grid } from "$lib/components"

	import ArcSlider from "./ArcSlider.svelte";
	import CaptionWindow from "./CaptionWindow.svelte";

	let videoElement;
	let videoWrapper;

	// These values are bound to properties of the video
	let time = writable(0); //i cant remember why i changed this
	let duration;
	let paused = true;
	let fullscreen = false;

	let showControls = true;
	let showControlsTimeout;

	let captionsState = "off" // can be off, basic or side

	export let fileSource = "";

    let thumbNailSource = fileSource+"/thumb";
	let subSource = fileSource+"/vtt";

	//fix when video player opening after new upload with previous id's thumbnail as poster? even though the video itself was correct
	$: thumbNailSource = fileSource+"/thumb";
	$: subSource = fileSource+"/vtt";

	let captionTrack;
	let customSubtitleText = "";
	let videoHeight;

	// Used to track time of last mouse down event
	let lastMouseDown;

	let allCaptionCues = [];

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

	function togglePlayback() {
		if(videoElement && paused){
			videoElement.play();
		}
		else if(videoElement) {
			videoElement.pause();
		}
	}

	// We cannot style the track element properly so we replace it with a regular div
	function onNewCue(event){
		let cueText = event?.target?.track?.activeCues[0]?.text;
		if(cueText){
			customSubtitleText = cueText;
		}
	}

	// Detect fullscreen changing externall6y from our functions.
	async function onFullscreenChange(e){
		fullscreen = !fullscreen;
	}

	async function goFullscreen(){
		if(!videoWrapper){
			return;
		}

		// These functions are broswer dependant, so we must check which one is declared to call it.
		if(videoWrapper.requestFullscreen){
			videoWrapper.requestFullscreen();
		} else if(videoWrapper.webkitRequestFullscreen){
			videoWrapper.webkitRequestFullscreen();
		} else if(videoWrapper.msRequestFullscreen){
			videoWrapper.msRequestFullscreen();
		}
	}


	async function exitFullscreen(){
		if(!videoElement){
			return;
		}
		
		// These functions are broswer dependant, so we must check which one is declared to call it.
		if(document.exitFullscreen){
			await document.exitFullscreen();
		} else if(document.webkitExitFullscreen){
			await document.webkitExitFullscreen();
		} else if(document.msExitFullscreen){
			await document.msExitFullscreen();
		}
	}

	async function toggleFullscreen(e){
		if(fullscreen){
			exitFullscreen();
		}
		else{
			goFullscreen();

			// Since user wants captions and side doesnt work in fullscreen we switch to basic
			if(captionsState == "side"){
				captionsState = "basic";
			}
		}
	}

	async function switchCaptions(e){
		switch (captionsState){
			case("off"):
				captionsState = "basic";
				break;
			case("basic"):
				captionsState = "side";
				break;
			case("side"):
				captionsState = "off";
				break;
		}

		// Captions on the side dont really make sense in a fullscreened video so stop the suer from switching to it
		if(fullscreen && captionsState == "side"){
			captionsState = "off";
		}
	}

	async function grabAllCaptions(event){
		if(event){
			let captions = [];
			let cues = event.target.track.cues;
			for (let index = 0; index < cues.length; index++) {
				let cue = cues[index];
				captions.push({
						content: cue.text,
						start: cue.startTime,
						end: cue.endTime,
					});
			}
			allCaptionCues = captions;
		}
	}

</script>
<div style="width: 100%; display: flex;">
<div class="default-video">
	<div bind:this={videoWrapper} bind:clientHeight={videoHeight} on:fullscreenchange={onFullscreenChange}> 
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
		bind:this={videoElement}
		crossorigin="anonymous"
		id="video"
		>
		<track kind="captions" id="dummy"/>
		<track kind="metadata" id="captionTrack" default src={subSource} bind:this={captionTrack} on:cuechange={onNewCue} on:load={grabAllCaptions}/>
	
		</video>
	
	

		<div class="controls" style="opacity: {duration && showControls ? 1 : 0}">
			<div class="video-captions" style="{captionsState === "basic" ? "display: block;" : "display: none;"}">{customSubtitleText}</div>
			<progress value={$time / duration || 0} />

			<div class="info">
				
				<div class="play-pause">
					<button on:click={togglePlayback} style="background-color: transparent; border-style: none;">
						<img src="{paused ? PlayIcon : PauseIcon}" alt="Click to {paused ? "play" : "pause"} the video"/>
					</button>
				</div>

				<div class="time">{formatToMins($time)}/{formatToMins(duration)}</div>\

				<div class="fullscreen-toggle">
					<button on:click={toggleFullscreen} style="background-color: transparent; border-style: none;">
						<img src="{fullscreen ? FullscreenExitIcon : FullscreenIcon}" alt="Click to {fullscreen ? "exit" : "enter"} fullscreen mode"/>
					</button>
				</div>

				<div class="play-pause">
					<button on:click={switchCaptions} style="background-color: transparent; border-style: none;">
						<img src="{captionsState == "off" ? CaptionsIcon : CaptionsActiveIcon}" alt="Click to activate captions"/>
					</button>
				</div>
			</div>
		</div>
	</div>
	

	
	<ArcSlider bind:time={$time} captionTrack={captionTrack} duration={duration}/>
</div>

{#if captionsState == "side"}
<div style="width: 25%; height: calc({videoHeight}px - 2rem); background-color: #393939; display: flexbox; padding: 1rem; border-radius: 8px">
	<CaptionWindow bind:currentTimeSeconds={$time} captions={allCaptionCues} maxTimeSeconds={duration}/>
</div>
{/if}


</div>
<style>
	div {
		position: relative;
	}

	track::after {
		color: red;
	}

	.controls {
		position: absolute;
		bottom: 0.5rem;
		width: 100%;
		transition: opacity 1s;
	}

	.info {
		display: flex;
		width: 100%;
		height: 3em;
	}

	.video-captions{
		color: #f4f4f4;
		font-family: Barlow;
		margin: auto;
		width: fit-content;
		font-size: xx-large;
	}

	.time {
		display: flexbox;
		color: #f4f4f4;
		font-family: Barlow;
		margin-top: auto;
		margin-bottom: auto;
	}

	.play-pause {
		display: flexbox;
		margin-top: auto;
		margin-bottom: auto;
	}

	.fullscreen-toggle {
		display: flexbox;
		margin-top: auto;
		margin-bottom: auto;
		margin-left: auto;
	}

	.default-video {
		width: 70%;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 0px;
		display: flexbox;

		height: 100vh;
		overflow-y: hidden;
		overflow-x: hidden;
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
