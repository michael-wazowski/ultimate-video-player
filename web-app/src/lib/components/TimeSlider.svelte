<script>
export let duration;
export let currentTimeSeconds;

export let onDragStart;
export let onDragEnd;

export let style;

</script>

<input on:mousedown={onDragStart} on:mouseup={onDragEnd} type="range" step="0.01" bind:value={currentTimeSeconds} min="0" max="{duration}" style="{style}"/>

<style>
    input {
        /* -webkit-appearance: none;
        appearance: none; */
        width: 100%;
        height: 4px;
        border-radius: 2px;
        margin: 0px;
        background: #6f6f6f;
        outline: none;
    }

    input::-webkit-slider-thumb {
        -webkit-appearance: none; /* Override default look */
        appearance: none;
        width: 15px; /* Set a specific slider handle width */
        height: 15px; /* Slider handle height */
        background: #0f62fe; /* Green background */
        cursor: pointer; /* Cursor on hover */
        border-radius: 50%;
    }

    input::-moz-range-thumb {
        width: 15px; /* Set a specific slider handle width */
        height: 15px; /* Slider handle height */
        background: #0f62fe; /* Green background */
        cursor: pointer; /* Cursor on hover */
        border-radius: 50%;
    }
</style>