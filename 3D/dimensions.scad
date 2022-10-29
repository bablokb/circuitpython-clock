// -----------------------------------------------------------------------------
// Dimensions for 3D prints. Adapt to your printer.
//
// Author: Bernhard Bablok
// License: GPL3
//
// https://github.com/bablokb/circuitpython-clock
//
// ---------------------------------------------------------------------------

$fa = 1;
$fs = 0.4;
$fn = 48;

fuzz = 0.01;
w2 = 0.86;                 // 2 walls Prusa3D
w4 = 1.67;                 // 4 walls Prusa3D
gap = 0.2;                 // gap pcb to case


// badger2040 specific dimensions   ------------------------------------------

rim = w4+ gap + w2 + gap;

x1_panel = 85.6 + 2*rim;           // outer dimension
x2_panel = 81.5 + rim;             // dimension full z-height
x3_panel = 66.9;                   // dimension inner cutout
x3_panel_off = 9.35 + rim;         //    offset

y1_panel = 48.7 + 2*rim;           // outer dimension
y2_panel = 39.3;                   // dimension full z-height
y3_panel = 29.06;                  // dimension inner cutout

z2_panel = 1.6;                    // panel depth above pcb
z3_panel = 0.4;                    // panel depth above display
z_panel  = z2_panel + z3_panel;

r_panel = 3;                       // panel rounding

d_panel_cyl      = 1.9;            // diameter cylinders for montage holes
h_panel_cyl      = 1.8;            // hight    cylinders for montage holes
xy_panel_cyl_off = 2.9 + rim;      // offsets center of holes

g_button     = 0.2;                // gap around buttons
x_button     = 4.2 + 2*g_button;   // width of button
x_button_off = 24;                 // offsets button a+c (from center)
y_button     = 3.2 + 2*g_button;   // depth of button
y_button_off = 7.27;               // offsets buttons up+down (from center)

x_led_off = 12.7 + rim;            // offset of activity-led
y_led_off = xy_panel_cyl_off;

x_wall = x1_panel - 2*w4 - 2*gap;  // outer wall dimensions
y_wall = y1_panel - 2*w4 - 2*gap;
z_wall = 15;

y_usb     =  9.00;                 // y-dim usb-c (mechanical drawing: 8.94)
y_usb_off = 10.15 + rim;           // offset from bottom
z_usb     =  5;

x_bb     = 17;                     // x-dim back buttons (min: 12.2)
x_bb_off = 14.5 + rim;             // offset from left
z_bb     = 10;

z_body = 30;                       // depth/height of the body

z_bcon     = z_body/3;             // base-connector
z_bcon_off = z_body/3;

x_cable = 10;                      // cable-hole
z_cable = 10;
