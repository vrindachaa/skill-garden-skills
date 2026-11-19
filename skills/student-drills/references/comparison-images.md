# Presentation derivatives for visual comparisons

Use when the course owner requests a background or other presentation-only change to existing before/after renders. This is not a new student build or replacement grading evidence.

## Procedure

1. Preserve original PNGs and saved scene files. Write derivatives into a separate `comparison/<presentation>/` directory; record source paths and transformations in a small manifest.
2. Check whether the source already has useful alpha. If so, composite it directly over the requested background with Pillow `Image.alpha_composite` or `Image.paste(..., mask=alpha)`.
3. For opaque renders, obtain a silhouette from the existing saved mesh. Do not solve the student's geometry or execute its build script again. Open its `.blend`, retain geometry/transforms, and reconstruct the exact source camera for each view from the actual rendering code or saved rig. Match projection, position, target, orthographic scale or lens, resolution and render percentage. A contact sheet may contain multiple camera poses even when the saved scene retains only the last camera.
4. Render mask PNGs locally with Blender Workbench and transparent film:

   ```python
   scene.render.engine = 'BLENDER_WORKBENCH'
   scene.render.film_transparent = True
   scene.render.image_settings.file_format = 'PNG'
   scene.render.image_settings.color_mode = 'RGBA'
   # Set the original view's camera and resolution before each render.
   bpy.ops.render.render(write_still=True)
   ```

   Do not save these presentation settings back into the submission `.blend`. Workbench is sufficient for an opaque mesh silhouette; matching original surface shading is unnecessary because its RGB will not be used.
5. Preserve original object pixels and replace only the background. For a tiled contact sheet, composite each source tile with its corresponding mask alpha, then place it back at the same offset:

   ```python
   from PIL import Image
   canvas = Image.new('RGB', source.size, background_rgb)  # requested RGB triple
   alpha = Image.open(mask_path).getchannel('A')
   tile = source.crop((x, y, x + width, y + height))
   canvas.paste(tile, (x, y), alpha)
   canvas.save(output_path)
   ```

6. Reopen/check dimensions, tile order and output existence. Use `vision_analyze` on both derivatives to confirm the requested background and intact surfaces, without turning a presentation check into a new identity grade.
7. Deliver the images inline with short Before/After labels and `MEDIA:` paths. Keep grading based on original evidence.

## Decision rules

- Use a saved-mesh silhouette when gray shading overlaps the background color; border-connected flood fill can leak into a surface through antialiasing and remove large interior regions.
- Reconstruct cameras from measured source settings, not a generic orbit recipe; even small scale/target mismatches can clip surfaces or leave gray fringes.
- Render only masks when the user requested only a background change; full shaded rerenders take longer and may change lighting, material appearance or the comparison itself.
- Treat antialiased edges as blended pixels, not proof of holes. Inspect whole surfaces and silhouettes before delivery.
- Keep presentation transformations symmetric across before/after; changing only one image introduces a display confound.
