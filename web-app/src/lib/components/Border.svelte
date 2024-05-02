<script>
    export let height = "100%";
    export let width = "100%";
    export let background = "transparent";
    export let corner = "0px";
    export let thickness = "0px";
    export let style = "";
</script>

<div style="height: {height}; width: {width}; background-color: {background}; border-radius: {corner}; border-width:{thickness}; {style}">
    <slot></slot>
</div>

<style>
</style>