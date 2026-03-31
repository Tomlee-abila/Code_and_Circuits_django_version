# Design System Strategy: Code & Circuits

## 1. Overview & Creative North Star
**Creative North Star: "The Electric Manuscript"**

This design system rejects the "standard dashboard" aesthetic in favor of a high-end, editorial STEM experience. It treats code and circuitry not as utility, but as digital art. By combining the stark, authoritative contrast of a luxury tech journal with the kinetic energy of "electric" accents, we create an environment that feels both academically rigorous and futuristically immersive.

To move beyond generic templates, this system utilizes **Intentional Asymmetry**. We break the rigid 12-column grid by allowing hero elements to bleed off-edge and using overlapping layers to create a sense of physical depth. The interface shouldn't feel like a flat website; it should feel like a high-powered IDE layered over a glowing schematic.

---

## 2. Colors: Tonal Depth & Kinetic Accents
The palette is built on a foundation of absolute darkness, allowing the primary yellow to act as a light source rather than just a color.

*   **Primary (The Current):** `primary` (#ffe483) and `primary_container` (#fdd400). Use these for high-action states.
*   **Surface Hierarchy (The Substrate):**
    *   `surface` (#0e0e0e): The base void.
    *   `surface_container_low` (#131313): Secondary background areas.
    *   `surface_container_highest` (#262626): Elevated interactive cards.

### The "No-Line" Rule
**Strict Mandate:** Designers are prohibited from using 1px solid borders to define sections. Layout boundaries must be achieved through:
1.  **Tonal Shifts:** Placing a `surface_container_high` card against a `surface_dim` background.
2.  **Negative Space:** Using the `spacing-16` or `spacing-24` tokens to create distinct "islands" of content.

### The "Glass & Gradient" Rule
To achieve the "electric" feel, all primary CTAs and active state indicators must use a subtle linear gradient from `primary` (#ffe483) to `primary_dim` (#edc600). For floating overlays (modals/tooltips), use a **Glassmorphism** effect: `surface_container_highest` at 80% opacity with a `20px` backdrop-blur.

---

## 3. Typography: Technical Authority
We pair the brutalist efficiency of **Space Grotesk** with the clinical precision of **Inter**.

*   **Display (Space Grotesk):** Used for "Hero" moments and section headers. High-contrast sizing (e.g., `display-lg` at 3.5rem) creates an editorial, bold impact.
*   **Body (Inter):** Used for all instructional content. It provides high legibility against dark backgrounds.
*   **Labels (Space Grotesk - All Caps):** Use `label-md` with 0.05em letter spacing for "Meta" data (e.g., "MODULE 01", "CIRCUIT STABILITY") to mimic technical blueprints.

---

## 4. Elevation & Depth: The Layering Principle
Forget drop shadows. In this system, depth is a product of **Tonal Layering**.

*   **Stacking Order:** Elements do not "float" with shadows; they "emerge" through brightness. An inner code editor should be `surface_container_lowest` (#000000) nested inside a `surface_container` (#1a1919) card, creating a "carved out" effect.
*   **The Ghost Border:** If a boundary is required for accessibility, use `outline_variant` at 15% opacity. It should be barely felt, acting as a whisper of a container rather than a box.
*   **Ambient Glow:** For the "Circuit" feel, active elements (like a selected lesson) may use an outer glow. This is not a shadow, but a `primary` colored blur (0px 0px 15px) at 20% opacity, mimicking the light emitted from a live wire.

---

## 5. Components: Precision Engineered

### Buttons
*   **Primary:** Solid `primary_container` with `on_primary` text. Sharp corners (`rounded-sm`). On hover, apply the "Electric Glow."
*   **Secondary:** Ghost style. No background, `outline` border at 20%, text in `primary`.
*   **Tertiary:** Text-only in `secondary_fixed`. Used for low-priority navigation.

### Cards & Lists
*   **The No-Divider Rule:** Never use a horizontal line to separate list items. Use a background shift to `surface_bright` on hover or `spacing-4` vertical gaps to define rows.
*   **Structure:** Cards use `rounded-md` (0.375rem). They should never have a 100% opaque border.

### Input Fields
*   **Default State:** `surface_container_highest` background, no border.
*   **Focus State:** A 1px `primary` bottom-border only, mimicking a terminal cursor. Text remains `on_surface`.

### Additional STEM Components
*   **The "Circuit Path":** A decorative or functional progress tracker using 1px `primary` lines that take 90-degree turns, connecting various lesson nodes.
*   **Code Block:** `surface_container_lowest` background with a `primary_fixed_dim` left-accent bar.

---

## 6. Do’s and Don’ts

### Do
*   **Do** use asymmetrical layouts where text is aligned left and imagery/interactive circuits are offset to the right.
*   **Do** lean into high-contrast "Display" typography for short, punchy headlines.
*   **Do** use `surface_container` tiers to create hierarchy.
*   **Do** ensure all "Electric" glows are subtle; if it looks like a neon sign, it's too much.

### Don’t
*   **Don’t** use 1px solid white or grey borders for sectioning.
*   **Don’t** use standard "drop shadows" (black at 20%). Only use tinted ambient glows.
*   **Don’t** use rounded corners larger than `xl` (0.75rem). This system is sharp and technical, not bubbly.
*   **Don’t** use "Generic Blue" for links. All interactive triggers are `primary` (yellow).