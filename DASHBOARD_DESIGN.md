# Mis-Selling Intelligence Platform - Dashboard Design

## Design Philosophy

**Mission**: Create a trustworthy, analytical, and authoritative interface for financial regulators to detect and monitor mis-selling risks.

**Design Principles**:
- **Clarity over Beauty**: Every element serves a purpose
- **Explainable Insights**: All data points can be traced back to sources
- **Zero Dark Patterns**: Transparent, honest UI
- **Long Reading Sessions**: Comfortable for extended analysis periods

---

## Design System

### Color Palette

**Primary Colors**:
- **Deep Navy**: `#1E293B` - Trust, authority, professionalism
- **Charcoal**: `#0F172A` - Sidebar background, depth

**Secondary Colors**:
- **Soft Gray**: `#F1F5F9` - Background, subtlety
- **White**: `#FFFFFF` - Card backgrounds, clarity

**Accent Colors** (Semantic):
- **Green** (`#10B981`): Aligned promises, low risk
- **Amber** (`#F59E0B`): Caution, medium risk
- **Red** (`#EF4444`): High mis-selling risk, critical alerts

**Neutral Colors**:
- **Text Primary**: `#0F172A`
- **Text Secondary**: `#64748B`
- **Border**: `#E2E8F0`

### Typography

**Font Family**: Inter (Google Fonts)
- Clean, modern, highly readable
- Professional appearance
- Excellent for long-form reading

**Hierarchy**:
- **H1**: 2rem (32px), Weight 700 - Main page titles
- **H2**: 1.5rem (24px), Weight 600 - Section headers
- **H3**: 1.125rem (18px), Weight 600 - Subsection headers
- **Body**: 1rem (16px), Weight 400 - Standard text
- **Small**: 0.875rem (14px) - Labels, captions

---

## Layout Structure

### Left Sidebar (Persistent Navigation)

**Branding Area**:
- Platform name: "Mis-Selling Intelligence"
- Subtitle: "Regulator Platform"
- Professional, minimal styling

**Navigation Items**:
1. Dashboard Overview
2. Products Monitor
3. Expectation Engine
4. Reality Engine
5. Risk Flags
6. Reports & Evidence
7. Settings

**System Status Indicator**:
- Real-time system health
- Visual status indicator

### Main Content Area

**Spacious Grid Layout**:
- Generous padding (2rem)
- Clear visual hierarchy
- Card-based component system
- Subtle shadows for depth

---

## Component Library

### 1. KPI Cards

**Purpose**: Display key performance indicators at a glance

**Features**:
- Clean card design with subtle shadows
- Large, readable numbers
- Trend indicators (↑ ↓ →)
- Color-coded trends (green/red/neutral)
- Hover effects for interactivity

**Usage Example**:
- Products Monitored: 25 (+2 this week)
- High-Risk Products: 3 (flagged)
- Average Risk Score: 0.42
- Customer Dissatisfaction: 28.5% (+2.3% vs last month)

### 2. Data Cards

**Purpose**: Present structured information in digestible chunks

**Features**:
- Clear headers with titles
- Metric rows with labels and values
- Subtle borders and shadows
- Consistent spacing

**Variants**:
- Standard data card
- Comparison card (side-by-side)
- Evidence card (with source attribution)

### 3. Risk Badges

**Semantic Status Indicators**:
- **Low Risk** (Green): Background `#D1FAE5`, Text `#065F46`
- **Medium Risk** (Amber): Background `#FEF3C7`, Text `#92400E`
- **High Risk** (Red): Background `#FEE2E2`, Text `#991B1B`
- **Critical Risk** (Red Border): Enhanced red with border

### 4. Comparison Panel

**Purpose**: Side-by-side comparison of promises vs reality

**Layout**:
- Two-column grid
- Left: "What Was Promised"
- Right: "Customer Reality"

**Visual Differentiation**:
- Match highlights: Green border-left
- Mismatch highlights: Red border-left
- Clear labeling for each aspect

### 5. Risk Meter

**Purpose**: Visual representation of risk scores (0-100)

**Features**:
- Horizontal bar with color gradient
- Numerical display
- Risk level badge
- Color-coded fill (green/amber/red)

### 6. Evidence Items

**Purpose**: Display supporting evidence with attribution

**Structure**:
- Source label (bold)
- Evidence text (italic, secondary color)
- Left border for visual hierarchy
- Clean spacing

---

## Page Layouts

### 1. Dashboard Overview

**Primary View**:
- Large title: "Mis-Selling Risk Overview"
- Subtitle: Description of purpose
- KPI cards (4-column grid)
- Risk distribution chart (pie)
- Top risk products list
- Expectation vs Reality comparison

**Purpose**: Provide immediate overview of system status

### 2. Products Monitor

**Features**:
- Search functionality
- Risk level filter
- Data table with sortable columns
- Product selection for detail view

**Purpose**: Monitor all analyzed products in real-time

### 3. Expectation Engine

**Tabs**:
- **Upload Document**: Drag & drop area for PDFs/brochures
- **Extracted Promises**: Structured promise profiles

**Promise Profile Shows**:
- Investment Objective
- Claimed Returns
- Risk Category
- Lock-in Period
- Exit Load/Fees
- NLP Confidence Score

**Purpose**: Extract and display promises from marketing materials

### 4. Reality Engine

**Components**:
- **Sentiment Timeline**: Rolling 30-day sentiment chart
- **CDI Gauge**: Customer Dissatisfaction Index (0-100)
- **Topic Breakdown**: Complaint categories with:
  - Mention frequency (%)
  - Sentiment polarity bar
  - Example anonymized quotes

**Purpose**: Analyze real customer experiences and sentiment

### 5. Risk Flags

**Components**:
- Product selector
- Risk score meter (0-100)
- "Why Flagged?" expandable section with:
  - Risk justification
  - Mismatch details
  - Evidence sources
- Evidence source cards with:
  - Data point counts
  - Average sentiment scores

**Purpose**: Detailed risk analysis and flagging justification

### 6. Reports & Evidence

**Features**:
- Report type selector
- Generate button
- Download functionality
- Report preview
- Report archive

**Purpose**: Generate regulator-ready reports and evidence packages

### 7. Settings

**Tabs**:
- Data Sources: Enable/disable feeds
- Alert Thresholds: Configure risk thresholds
- System: Format preferences

**Purpose**: Configure system behavior and preferences

---

## Interaction Patterns

### Navigation
- Click-based navigation between sections
- Active state highlighting
- Smooth transitions
- No unnecessary animations

### Data Display
- Tables with clean styling
- Expandable sections for details
- Hover states for interactivity
- Loading states for async operations

### User Actions
- Clear call-to-action buttons
- Primary actions highlighted
- Confirmation for critical actions
- Success/error feedback

---

## Visual Guidelines

### Spacing
- Generous whitespace for clarity
- Consistent padding (1rem, 1.5rem, 2rem)
- Clear section dividers

### Shadows
- Subtle shadows for depth
- `shadow-sm`: 0 1px 2px rgba(0,0,0,0.05)
- `shadow-md`: 0 4px 6px rgba(0,0,0,0.1)
- `shadow-lg`: 0 10px 15px rgba(0,0,0,0.1)

### Borders
- Thin borders (1px) for separation
- Border-radius: 6px-8px for cards
- Consistent border colors

### Icons
- Minimal icon usage
- Professional, simple icons
- No cartoon or flashy icons
- Semantic icons only

---

## Accessibility

### Color Contrast
- All text meets WCAG AA standards
- High contrast for readability
- Color not the sole indicator

### Typography
- Readable font sizes
- Clear hierarchy
- Adequate line spacing

### Interactive Elements
- Clear focus states
- Adequate click targets
- Keyboard navigation support

---

## Performance Considerations

### CSS
- Efficient selectors
- Minimal animations
- Optimized for rendering

### JavaScript
- Minimal Streamlit overhead
- Efficient data loading
- Lazy loading where appropriate

---

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Streamlit-compatible rendering
- Responsive design principles

---

## Future Enhancements

### Potential Additions
1. Dark mode toggle
2. Custom date range selectors
3. Advanced filtering options
4. Export to Excel/CSV
5. Real-time updates with WebSocket
6. Customizable dashboard widgets
7. Annotation system for reports
8. Collaboration features

---

## Implementation Notes

### Streamlit-Specific
- Uses custom CSS injection
- Leverages Streamlit components where possible
- Maintains Streamlit state management
- Compatible with Streamlit deployment

### Data Integration
- Loads from CSV files (pipeline outputs)
- Handles missing data gracefully
- Provides helpful error messages
- Shows loading states

### Custom Components
- All styled with custom CSS
- Professional, consistent appearance
- Accessible and usable
- Maintainable code structure

---

## Design Philosophy Summary

This dashboard embodies:

✅ **Trust**: Professional, authoritative appearance  
✅ **Clarity**: Every element has a purpose  
✅ **Transparency**: All insights are explainable  
✅ **Efficiency**: Built for long reading sessions  
✅ **Reliability**: No flashy gimmicks, just solid design  

**Result**: A regulator-grade interface that financial authorities can trust for real-world decision-making.

---

*Design System Version: 1.0*  
*Last Updated: 2025-01-12*
