/**
 * @param {LGraphNode} node 
 * @param {CanvasRenderingContext2D} ctx 
 * @param {HTMLImageElement} img 
 */
 function drawImageInClientArea(node, ctx, img) {
    const y = node.computeSize()[1];

    const availableWidth = node.size[0];
    const availableHeight = node.size[1] - y;

    const scale = Math.min(availableWidth / img.width, availableHeight / img.height);
    const x_off = Math.floor((availableWidth - img.width * scale) / 2);
    const y_off = Math.floor((availableHeight - img.height * scale) / 2);

    ctx.save();
    ctx.translate(x_off, y + y_off);
    ctx.scale(scale, scale);
    ctx.drawImage(img, 0, 0);
    ctx.restore();
}

/**
 * @param {CanvasRenderingContext2D} ctx
 */
function NodeWithPreview_onDrawBackground(ctx) {
    if (this.flags.collapsed) {
        return;
    }
    if (this.img && this.size[0] > 5 && this.size[1] > 5) {
        drawImageInClientArea(this, ctx, this.img);
    }
};

/**
 * @param {CanvasRenderingContext2D} ctx
 */
 function NodeWithPreview_onProcessingResults(res) {
    this.img = document.createElement("img");
    this.img.src = "data:" + res.preview;

    this.img.onload = () => {
        this.setDirtyCanvas(true);
    };
}
