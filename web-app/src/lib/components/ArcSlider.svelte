<script>
	import { tweened } from "svelte/motion";
	import { pannable } from "../core/pannable";

	export let trackColor = "";
	export let thumbColor = "";
	export let height = 0;
	export let thumbWidth = 5;
	export let thumbHeight = 25;

	/*
	// Represents the percentage of the track from the left to the right where the thumb is, from 0 to 1 representing 0-100
	export let positionPercentage = 0;

	const coords = { x: 0, y: 0, xP: 0};

	let maxRadius = 500;
	let maxHeight = height <= 0 ? 60 : height;
	let containerWidth = maxRadius*2;
	
	function handlePanStart() {
		coords.stiffness = coords.damping = 1;
	}

	// postionPercentage is for binding externally to control the position of the thumb, we need to handle when it is changed externally.
	$: if(positionPercentage != coords.xP){
		coords.xP = positionPercentage;
		coords.x = (coords.xP * containerWidth) - (containerWidth/2);
		coords.y = getElipsicalY()*-1;
	}
	
	$: if(containerWidth){
		maxRadius = containerWidth/2;
		coords.x = (coords.xP * containerWidth) - (containerWidth/2);
	}

	// https://www.khanacademy.org/math/precalculus/x9e81a4f98389efdf:conics/x9e81a4f98389efdf:ellipse-center-radii/a/ellipse-equation-review
	function getElipsicalY() {
		let x = coords.x*coords.x;
		let a = maxRadius*maxRadius;
		let b = maxHeight*maxHeight;
		return Math.sqrt(Math.abs(((b*x)/a) - b));
	}
	
	function handlePanMove(event) {
		if(coords.x + event.detail.dx > maxRadius){
			coords.x = maxRadius;
			coords.y = getElipsicalY()*-1;
			return;
		}
		if(coords.x + event.detail.dx < -maxRadius){
			coords.x = -maxRadius;
			coords.y = getElipsicalY()*-1;
			return;
		}
		
		coords.x = coords.x + event.detail.dx;
		coords.xP = (coords.x + containerWidth * 0.5) / containerWidth;
		positionPercentage = coords.xP;
		coords.y = getElipsicalY()*-1;
	}

	function handlePanEnd(event) {
		//coords.x = 0;
		//coords.y = getElipsicalY()*-1;
	}
*/

	let maxRadius = 500;
	let maxHeight = height <= 0 ? 60 : height;
	let containerWidth = maxRadius * 2;

	export let time;
	export let captionTrack;
	export let duration;

	//all of the events from the captions marked with "IP" (interest point)
	let sliderEvents = [];

	//all of the events from slider events currently visible
	let visibleSliderEvents = [];
	//let visibleSliderEvents = [{content: "Text",time: 10},{content: "Text2", time: 30},{content: "Text3", time: 60},{content: "Text4", time: 120}];
	//let visibleSliderEvents = [{content: "Text2", angle: 25.8419, time: 120}];

	function handlePanStart() {
		//update the mouse cursor css
	}

	$: if (containerWidth) {
		maxRadius = containerWidth / 2;
	}

	function handlePanMove(event) {
		//what is the new time going to be
		//minus because the mouse moves left = time goes forward
		//division by 300 just a rough estimate, mouse movement feels pretty 1:1 with the resulting rotation
		let proposedTime = time - event.detail.dx * ($currentTimeScale / 300);

		//dont run off the end of the video
		if (proposedTime < 0) {
			proposedTime = 0;
		} else if (proposedTime > duration) {
			proposedTime = duration;
		}

		//update the actual time
		time = proposedTime;
	}

	function handlePanEnd(event) {
		//update the mouse cursor css
	}

	//get each of the cues from captionTrack with id = "IP"
	function processCaptionTrack() {
		if (typeof captionTrack != "undefined") {
			let cues = captionTrack.track.cues;

			for (let index = 0; index < cues.length; index++) {
				const cue = cues[index];

				if (cue.id == "IP") {
					console.log(cue.id);
					sliderEvents.push({
						content: cue.text,
						time: cue.startTime,
					});
				}
			}
		}
	}

	//this is copied from VideoPlayer, is there some way to use that ones function without having to redefine here?
	function format(seconds) {
		if (isNaN(seconds)) return "...";

		const minutes = Math.floor(seconds / 60);
		seconds = Math.floor(seconds % 60);
		if (seconds < 10) seconds = "0" + seconds;

		return `${minutes}:${seconds}`;
	}

	//When time changes, figure out the state of our chips
	$: handleTime(time);

	//Force it to change when page loads (this relies on captionTrack loading fast)
	setTimeout(() => {
		time += 0.0001;
	}, 50);

	let processed = false;

	//TODO
	//dynamic timescale (base off of min angle between points?)
	//moving backwards
	async function handleTime(timeV) {
		//pull all of the cues into an array (the cue list isn't actually an array)
		if (sliderEvents.length == 0 && !processed) {
			processCaptionTrack();
			console.log("Process caption track");
		} else {
			processed = true;
		}

		//look at the oldest time, is it still within timescale
		//if not, remove it
		if (visibleSliderEvents.length > 0) {
			if (visibleSliderEvents[0].time < timeV - $currentTimeScale) {
				console.log("late");
				visibleSliderEvents = visibleSliderEvents.slice(1);
			}
		}

		//if we dont have enough events on the slider, get more
		if (visibleSliderEvents.length < 3 && sliderEvents.length > 1) {
			//i dont like this line of code
			while (sliderEvents[0].time < timeV + $currentTimeScale) {
				visibleSliderEvents.push(sliderEvents[0]);

				sliderEvents = sliderEvents.slice(1);

				//console.log(visibleSliderEvents, sliderEvents);
			}
		}

		if (visibleSliderEvents.length > 0 && sliderEvents.length > 0) {
			if (
				visibleSliderEvents[visibleSliderEvents.length - 1].time < timeV
			) {
				console.log("hi");
				$currentTimeScale = sliderEvents[0].time - timeV;
				visibleSliderEvents.push(sliderEvents[0]);
				sliderEvents = sliderEvents.slice(1);
			}
		}
	}

	//delta between current timestamp and most forward point on the graph
	let currentTimeScale = tweened(60, { duration: 500 });

	//want to restructure the divs so this doesn't need to be estimated
	//let y = 0.9
	//let x=Math.sqrt(1-(y*y))
	let endAngle = 35; //90 - (Math.atan(y/x) * 180 / Math.PI);

	//haven't got dynamic timescale happening yet
	function handleClick() {
		//sets the target to tween() towards
		$currentTimeScale = 240;
	}
</script>

<!-- old code for box being the scrollable element on top of a squished elipse 
	
	<div class="container" bind:offsetWidth={containerWidth}>
<div class = "elipse-path" style="--elipse-width: {maxRadius*2}px; --elipse-height: {maxHeight*2}px; border-color:{trackColor};">
</div>

<div
	class="box"
	use:pannable
	on:panstart={handlePanStart}
	on:panmove={handlePanMove}
	on:panend={handlePanEnd}
	style="transform:
		translate({coords.x}px,{coords.y}px); background-color:{thumbColor}; --width:{thumbWidth}px; --height:{thumbHeight}px;"
/>
</div> -->

<!-- code for the boxes rendered from js, but still on the squished curve (inside pannable)
		
		<div
		class="box"
		style="transform:
			translate({coords.x}px,{coords.y}px); background-color:{thumbColor}; --width:{thumbWidth}px; --height:{thumbHeight}px;"
	/> 
	
	{#each visibleSliderEvents as chip}
		<div class="box" style="transform:
		translate({coords.x}px,{coords.y}px); background-color:{thumbColor}; --width:{thumbWidth}px; --height:{thumbHeight}px;">{chip.content}</div>
	{/each} -->

<div class="container" bind:offsetWidth={containerWidth}>
	<div
		use:pannable
		on:panstart={handlePanStart}
		on:panmove={handlePanMove}
		on:panend={handlePanEnd}
		class="elipse-path"
		id="elipsePath"
		style="--elipse-width: {maxRadius * 2}px; --elipse-height: {maxHeight *
			2}px; border-color:{trackColor};"
	></div>

	<div
		class="rotator"
		style="--elipse-width: {maxRadius * 2}px; --elipse-height: {maxHeight *
			2}px; border-color:{trackColor};"
	>
		<div
			class="box"
			style="transform:
			translate(0px,-15px); background-color:{thumbColor}; --width:{thumbWidth}px; --height:{thumbHeight}px;"
		>
			<div class="boxText">
				<br><br><br>
				{format(time)}
			</div>
		</div>
	</div>

	{#each visibleSliderEvents as chip}
		<div
			class="rotator"
			style="rotate: {((chip.time - time) / $currentTimeScale) *
				endAngle}deg ;--elipse-width: {maxRadius *
				2}px; --elipse-height: {maxHeight *
				2}px; border-color:{trackColor};"
		>
			<div
				class="box"
				style="transform: translate(0px,-15px); background-color:{thumbColor}; --width:{thumbWidth}px; --height:{thumbHeight}px;"
			>
				<div class="boxText">
					{format(chip.time)}
					<br />
					{chip.content.slice(0, 20)}
				</div>
			</div>
		</div>
	{/each}
</div>

<button on:click={handleClick} style="transform-origin: 0 0">
	test button changes timescale
</button>

<style>
	* {
		--elipse-width: 1000px;
		--elipse-height: 120px;
		--track-width: 4px;
	}

	.box {
		--width: 15px;
		--height: 25px;
		position: absolute;
		width: var(--width);
		height: var(--height);
		left: calc(50% - var(--width) / 2);
		/*top: calc(50% - var(--height) / 2);*/
		border-radius: calc(var(--width) / 2);
		background-color: #ff3e00;
		cursor: move;
		color: white;
	}

	.boxText {
		width: 80px;
		text-align: center;
		position: absolute;
		left: 50%;
		top: 50%;
		transform: translate(-50%, 25%);
		font-size: 15px;
	}

	.elipse-path {
		background-color: transparent;
		/*width: calc(var(--elipse-width) - var(--track-width)*2);
		height: var(--elipse-height);*/
		border-width: var(--track-width);
		border-color: white;
		border-style: solid;
		border-radius: 50%;
		position: absolute;
		left: calc(50% - var(--elipse-width) / 2);
		top: calc(50% - var(--elipse-height) / 2 - var(--track-width) / 2);

		clip-path: inset(0px 0px 90%);

		width: 100%;
		aspect-ratio: 1 / 1;

		cursor: grab;
		/* todo make this change on click */
	}

	.rotator {
		background-color: transparent;
		width: 100%;
		border-width: var(--track-width);
		border-color: rgba(255, 255, 255, 0);
		border-style: solid;
		border-radius: 50%;
		position: absolute;
		left: calc(50% - var(--elipse-width) / 2);
		top: calc(50% - var(--elipse-height) / 2 - var(--track-width) / 2);
		aspect-ratio: 1 / 1;
		pointer-events: none;
		/*transition: rotate 1s;*/
	}

	.container {
		padding-top: 200px;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}
</style>
