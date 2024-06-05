<script>
    import { writable } from "svelte/store";
	import { fade } from "svelte/transition";
	import { onMount } from 'svelte';
	import { formatToMins } from "$lib/core/formatting";
	import PlayIcon from "$lib/assets/play-icon.svg";
	import PauseIcon from "$lib/assets/pause-icon.svg";
	import FullscreenIcon from "$lib/assets/fullscreen-icon.svg";
	import FullscreenExitIcon from "$lib/assets/fullscreen-exit-icon.svg";
	import CaptionsIcon from "$lib/assets/captions-icon.svg";
	import CaptionsActiveIcon from "$lib/assets/captions-active-icon.svg";
	import OcrIcon from "$lib/assets/ocr-icon.svg";
	import OcrActiveIcon from "$lib/assets/ocr-active-icon.svg";


    //import { Border, Grid } from "$lib/components"

	import ArcSlider from "./ArcSlider.svelte";
	import CaptionWindow from "./CaptionWindow.svelte";
	import TimeSlider from "./TimeSlider.svelte";
	import Grid from "./Grid.svelte";

	let videoElement;
	let videoWrapper;

	// These values are bound to properties of the video
	let time = writable(0); //i cant remember why i changed this
	let duration;
	let paused = true;
	let fullscreen = false;

	let controlsHovered = false;
	let videoHovered = false;	
	let videoHoveredTimeout;

	let captionsState = "off" // can be off, basic or side
	let ocrState = "off" // can be off or side
	let playbackRate = 1

	export let fileSource = "";

    let thumbNailSource = fileSource+"/thumb";
	let subSource = fileSource+"/stt";
	let ocrSource = fileSource+"/ocr"

	//fix when video player opening after new upload with previous id's thumbnail as poster? even though the video itself was correct
	$: thumbNailSource = fileSource+"/thumb";
	$: subSource = fileSource+"/stt";
	$: ocrSource = fileSource+"/ocr"

	let customSubtitleText = "";
	let customOCRText = "";
	let currentCueStartTime;
	let currentOcrStartTime;
	let videoHeight;

	// Used to track time of last mouse down event
	let lastMouseDown;

	let allCaptionCues = [];
	let allOCRCues = [];


	async function onVideoError(e){
		console.log("rbuhg");
	}

	async function onVideoHovered(e){
		videoHovered = true;
		clearTimeout(videoHoveredTimeout);
		videoHoveredTimeout = setTimeout(() => {videoHovered = false;}, 3000);
	}

	async function onControlsExit(e){
		controlsHovered = false;
		onVideoHovered();
	}

	async function onControlsEnter(e){
		controlsHovered = true;
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
		currentCueStartTime = event?.target?.track?.activeCues[0]?.startTime;
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
			if(ocrState === "side"){
				ocrState = "off";
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

	async function switchOcr(e){
		switch (ocrState){
			case("off"):
				ocrState = "side";
				break;
			case("side"):
				ocrState = "off";
				break;
		}
	}

	async function switchPlaybackRate(e){
		playbackRate += 0.25
		if (playbackRate > 2){
			playbackRate = 0.25
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
						id: cue.id
					});
			}
			allCaptionCues = captions;
		}
	}

	async function grabAllOCR(event){
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
			allOCRCues = captions;
		}
	}

	function onNewOcrCue(event){
		currentOcrStartTime = event?.target?.track?.activeCues[0]?.startTime;
	}

	async function onKeypress(e){

		const activeElement = document.activeElement;
    		if (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA') {
        	return; // Exit the function if the keypress is within an input or textarea
    	}

		switch(e.code){
			case("Space"):
				togglePlayback();
				e.preventDefault();
				break;
			case("KeyC"):
				switchCaptions();
				break;
			case("KeyF"):
				toggleFullscreen();
				break;
			case("KeyR"):
				switchOcr();
				break;
		}
	}

</script>
<svelte:window on:keydown={onKeypress}/>
<div style="width: 100%; display: flex; align-content: flex-start;">
<div class="default-video">
	<div role="presentation" bind:this={videoWrapper} bind:clientHeight={videoHeight} on:fullscreenchange={onFullscreenChange} on:focus={(e) => {}} on:mouseenter={onVideoHovered} style="display: inline-block;"> 
		<video
		poster={thumbNailSource}
		src={fileSource}
		on:mousedown={handleMousedown}
		on:mouseup={handleMouseup}
		on:error={onVideoError}
		bind:currentTime={$time}
		bind:duration
		bind:paused
		bind:this={videoElement}
		bind:playbackRate={playbackRate}
		crossorigin="anonymous"
		id="video"
		>
		<track kind="captions" id="dummy"/>
		<track kind="metadata" id="ocrTrack" default src={ocrSource} on:load={grabAllOCR} on:cuechange={onNewOcrCue}/>
		<track kind="metadata" id="captionTrack" default src={subSource} on:cuechange={onNewCue} on:load={grabAllCaptions}/>

		</video>
	
	
		<div role="presentation" class="controls" on:focus={(e) => {}} on:mouseenter={onControlsEnter} on:mouseleave={onControlsExit}>
			{#if captionsState === "basic"}
			<div transition:fade class="video-captions">{customSubtitleText}</div>
			{/if}


			{#if (duration && (controlsHovered || paused || videoHovered))}
			<div transition:fade style="background: linear-gradient(to top, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0)); border-radius: inherit;">
				<TimeSlider bind:currentTimeSeconds={$time} duration={duration} onDragStart={(e) => {videoElement.pause();}}/>

				<div class="info">
					<div>
						<div>
							<button on:click={togglePlayback} style="background-color: transparent; border-style: none;">
								<img src="{paused ? PlayIcon : PauseIcon}" alt="Click to {paused ? "play" : "pause"} the video" style="vertical-align: middle;"/>
							</button>
						</div>
		
						<div class="text">{formatToMins($time)}/{formatToMins(duration)}</div>
					</div>
					
					<div >
						<div>
							<button on:click={switchPlaybackRate} style="background-color: transparent; border-style: none;" class="text">
								{playbackRate}x
							</button>
						</div>
						<div>
							<button on:click={switchCaptions} style="background-color: transparent; border-style: none;">
								<img src="{captionsState == "off" ? CaptionsIcon : CaptionsActiveIcon}" alt="Click to activate captions" style="vertical-align: middle;"/>
							</button>
						</div>
						<div>
							<button on:click={switchOcr} style="background-color: transparent; border-style: none;">
								<img src="{ocrState == "off" ? OcrIcon : OcrActiveIcon}" alt="Click to activate ocr" style="vertical-align: middle;"/>
							</button>
						</div>
						<div>
							<button on:click={toggleFullscreen} style="background-color: transparent; border-style: none;">
								<img src="{fullscreen ? FullscreenExitIcon : FullscreenIcon}" alt="Click to {fullscreen ? "exit" : "enter"} fullscreen mode" style="vertical-align: middle;"/>
							</button>
						</div>
					</div>

				</div>
			</div>
		
			{/if}
		</div>
	</div>
	
	
	<ArcSlider bind:time={$time} allCaptionCues={allCaptionCues} duration={duration}/>
</div>

{#if captionsState === "side" || ocrState === "side"}
<div style="width: 25%; height: {videoHeight}px; display: flex; flex-direction: column; gap: 10px; justify-self: left;" transition:fade>
		{#if captionsState === "side"}
			<CaptionWindow bind:currentTimeSeconds={$time} captions={allCaptionCues} currentCueStartTime={currentCueStartTime}/>
		{/if}
		{#if ocrState === "side"}
			<CaptionWindow bind:currentTimeSeconds={$time} captions={allOCRCues} currentCueStartTime={currentOcrStartTime}/>
		{/if}
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
		bottom: 0px;
		width: 100%;
		border-radius: 10px;
	}

	.info {
		display: flex;
		width: 100%;
		height: 3em;
		justify-content: space-between;
	}

	.info .text {
		color: #f4f4f4;
		font-family: Barlow;
		font-size: 18px;
	}

	.info > div {
		display: flex;
		flex-direction: row;
	}

	.info > div > div {
		margin-top: auto;
		margin-bottom: auto;
	}

	.video-captions{
		color: #f4f4f4;
		background-color: rgba(0, 0, 0, 0.7);
		padding-left: 10px;
		padding-right: 10px;
		font-family: Barlow;
		height: fit-content;
		margin: auto;
		width: fit-content;
		font-size: xx-large;
		border-radius: 8px;
		margin-bottom: 1%;
	}	

	.default-video {
		width: initial;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 0px;

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
		border-radius: 10px 10px 10px 10px;
		display: block;
	}
</style>
