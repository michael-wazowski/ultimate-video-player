<script>
    export let columns = "1fr";
    export let rows = "1fr";
    export let height = "100%";
    export let width = "100%";
    export let style = "";
</script>

<div class="grid" style="grid-template-columns: {columns}; grid-template-rows: {rows}; height: {height}; width: {width}; {style}">
    <slot></slot>
</div>

<style>
.grid{
    display: grid;
}
</style>