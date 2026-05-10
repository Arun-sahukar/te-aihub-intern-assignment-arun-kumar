# Edge Cases in Blood Cell Annotation

## Overview
This document describes how to handle common edge cases encountered when annotating BCCD blood cell images.

## 1. Overlapping Cells

### Problem
Red blood cells often overlap or stack on top of each other, making individual cell boundaries unclear.

### Guidelines
- **Partial overlap (< 50%)**: Draw separate bounding boxes for each visible cell
- **Significant overlap (> 50%)**: Draw one box around the cluster if individual cells cannot be distinguished
- **Stacked cells**: Annotate the topmost visible cell; skip completely hidden cells

### Example Decision
```
Two RBCs with 30% overlap:
[ RBC-1 ] [ RBC-2 ]  <- Draw two separate boxes

Cluster of 5+ overlapping RBCs:
[  Cluster  ]  <- Draw one larger box if individuals are indistinguishable
```

## 2. Tiny Platelets

### Problem
Platelets are very small and can be confused with image artifacts or debris.

### Guidelines
- **Minimum size**: Only annotate platelets that are at least 5x5 pixels visible
- **Identification**: Platelets typically appear as small purple/violet dots
- **Clusters**: Platelet aggregates should be annotated as a single bounding box
- **Skip**: Do not annotate debris, staining artifacts, or unclear tiny dots

### Visual Cues for Platelets
- Purple/violet color (Giemsa stain)
- Irregular or round shape
- Smaller than RBCs (about 1/3 to 1/4 the size)
- Often found near WBCs or in clusters

## 3. Unclear Objects

### Problem
Some objects may be ambiguous - unclear cell type or possibly artifacts.

### Guidelines
- **50% confidence rule**: Only annotate if you are at least 50% confident it's a cell
- **When in doubt**: Skip the object rather than guess incorrectly
- **Artifacts to skip**:
  - Dust particles
  - Staining irregularities
  - Out-of-focus areas
  - Air bubbles

### Decision Framework
```
Is it a cell? 
├── Clearly yes → Annotate with appropriate label
├── Probably yes (>50%) → Annotate with best guess
└── Unclear (<50%) → Skip (do not annotate)
```

## 4. Partial Objects at Image Borders

### Problem
Cells at the edges of the image may be partially cut off.

### Guidelines
- **> 50% visible**: Annotate with a bounding box covering the visible portion
- **< 50% visible**: Do not annotate (too little information)
- **Bounding box**: Should fit only the visible portion, not extend beyond image boundaries

### Examples
```
Image border
│
│ [RBC half visible]  <- Annotate (>50% visible)
│ 
│[tiny edge]  <- Skip (<50% visible)
```

## 5. WBC Identification

### Problem
WBCs are less common and must be correctly distinguished from RBCs.

### Key Identifiers for WBCs
- **Larger size**: 2-3x diameter of RBCs
- **Visible nucleus**: Dark purple/blue stained nucleus
- **Irregular shape**: Not perfectly circular like RBCs
- **Cytoplasm**: May show granules or specific coloring

### Common WBC Types in BCCD
- Neutrophils (most common)
- Lymphocytes
- Monocytes
- Eosinophils
- Basophils

## 6. RBC Variations

### Normal Variations to Annotate
- Slightly oval RBCs
- Crenated (spiky edge) RBCs
- Overlapping RBCs

### Do Not Annotate
- Ghost cells (very faint/lysed)
- Severely damaged cells
- Unidentifiable fragments

## 7. Annotation Consistency Rules

### Bounding Box Tightness
- Box should touch the cell edges with minimal padding
- Consistent 1-2 pixel margin is acceptable
- Avoid excessive whitespace in boxes

### Labeling Priority
When a cell could potentially be multiple types:
1. If clearly identifiable → Use correct label
2. If WBC vs artifact → Default to skip
3. If RBC vs debris → Default to skip

## 8. Summary Decision Table

| Situation | Action |
|-----------|--------|
| Clear cell, fully visible | Annotate normally |
| Overlapping cells (<50%) | Separate boxes |
| Overlapping cells (>50%) | Single box or skip |
| Platelet > 5px | Annotate |
| Platelet < 5px | Skip |
| Border cell >50% visible | Annotate visible part |
| Border cell <50% visible | Skip |
| Unclear object | Skip |
| Obvious artifact | Skip |

## Notes
- Consistency is more important than perfection
- When in doubt, document the decision and apply it consistently
- Review these guidelines before each annotation session
