# Illustration prompts

Use the host's image-reference mechanism to attach the chosen sheet. Merely
mentioning its filename does not attach an image. If it cannot be attached,
describe the inspected panel precisely and disclose that limitation.

Build the prompt in this order:

1. **Purpose:** audience, one takeaway, language and output ratio.
2. **Reference role:** sheet filename, exact panel ID and position. Treat it as a
   style reference by default; list fixed layout features only when the user
   explicitly requests them. State whether the output is one complete figure or
   a requested multi-panel sheet.
3. **Content and composition:** exact title, labels, entities and groups. Describe
   a layout designed around their actual relationships, with independently chosen
   positions, shapes and counts. Do not transplant a panel's silhouette or layers
   merely because it was selected as a reference.
4. **Visual treatment:** retain the reference's color hierarchy, gradients,
   typography, fine contours, translucent surfaces, subtle shadows and whitespace.
   Describe concrete observed features to guide rendering without fixing layout.
5. **Relationships:** each arrow's source, target and meaning. Distinguish leaders,
   membership lines, support arrows, forward sequence and feedback.
6. **Data and quality:** actual values/units/source if applicable; correctness,
   legibility and visual match. Quantitative marks require verified geometry.

Replace all example business text. Sheet headers and panel IDs are navigation
and must not appear in the user's final illustration unless requested. The
reference supplies the visual language and quality standard; the user's source
supplies the facts and relationships that determine structure. Match a specific
layout only when explicitly requested.

## Rendering paths

For native image generation, attach the reference image and identify its style
role separately from the new composition. For code drawing, derive nodes, groups,
edges and coordinates from the content and label sizes, then apply the visual
treatment through SVG/CSS or the available drawing library. Preserve editable
text where supported and verify actual font coverage. Both paths follow the same
style-versus-layout rules; disclose unsupported material effects.

## Example: style reference with a new layout

> 为中文技术文章生成一张 16:9 配图，标题为“事件总线连接同级服务”。
> 附图 `layered-02.png` 右下角 L08 用于参考视觉风格：青蓝至钴蓝与靛蓝的
> 色阶、半透明薄面、精细轮廓、淡紫柔和投影、简洁图标与清晰文字。
> 根据下面的关系独立设计构图，采用中心总线与周围三个同级服务的网络布局。
>
> 中央节点为“事件总线”，周围三个等权节点为“检索服务”“分析服务”
> “通知服务”。每个服务都向总线发布事件，也从总线订阅事件；分别用两条
> 方向相反的细线箭头表达，标注“发布”和“订阅”。服务之间没有直接连接。
> 节点大小相当，留出连线通道，以色阶、细边和柔和阴影形成精致的空间层次。
> 图中只出现上述标题、节点和关系标签。检查三个服务地位平等、箭头方向准确、
> 中文清楚，以及整体配色、线条和材质与参考图一致。

## Handoff

For a prompt-only request, return the production prompt. Otherwise render and
inspect the actual output against the reference and source, then deliver the
file/image with a short caption. If rendering fails, state the failure and retain
the prompt as a fallback; do not claim an image was produced.
