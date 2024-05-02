<script>
	import { spring } from 'svelte/motion';
	import { pannable } from '../core/pannable';

	const coords = { x: 0, y: 0, xP: 0};
	export let trackColor = "";
	export let thumbColor = "";
	export let height = 0;
	export let thumbWidth = 15;
	export let thumbHeight = 25;
	// Represents the percentage of the track from the left to the right where the thumb is, from 0 to 1 representing 0-100
	export let positionPercentage = 0;
	
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
</script>

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
</div>

	
<style>
	* {
		--elipse-width: 1000px;
		--elipse-height: 120px;
		--track-width: 8px;
	}
	
	.box {
		--width: 15px;
		--height: 25px;
		position: absolute;
		width: var(--width);
		height: var(--height);
		left: calc(50% - var(--width) / 2);
		top: calc(50% - var(--height) / 2);
		border-radius: calc(var(--width) / 2);
		background-color: #ff3e00;
		cursor: move;
	}

	.elipse-path {
		background-color: transparent;
		width: calc(var(--elipse-width) - var(--track-width)*2);
		height: var(--elipse-height);
		border-width: var(--track-width);
		border-color: white;
		border-style: solid;
		border-radius: 50%;
		position: absolute;
		left: calc(50% - var(--elipse-width)/2);
		top: calc(50% - var(--elipse-height)/2 - var(--track-width)/2);
		clip-path: inset(0px 0px 50%);
	}

	.container {
		padding-top: 200px;
		width: 100%;
		height: 100%;
	}
</style>