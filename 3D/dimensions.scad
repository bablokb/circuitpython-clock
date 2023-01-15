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

rim = w4 + gap/2 + w2 + gap;       // outer walls, gap/2, inner walls, gap

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

x_wall = x1_panel - 2*w4 - gap;    // inner wall dimensions (outside)
y_wall = y1_panel - 2*w4 - gap;
z_wall = 10.2;

y_usb     = 13.00;                 // y-dim usb-c (for plugs with larger shields)
y_usb_off = 10.15 + rim;           // offset from bottom
z_usb     = 8.5;

x_bb     = 15.5;                   // x-dim back buttons (min: 12.2)
y_bb     =  3.2 + rim;             // badger-boarder to inner side of buttons
x_bb_off = 14.5 + rim;             // offset from left
h_bb     =  5;                     // cover height
h_bb_off = 1.8;
z_bb     = h_bb+x_bb-2*w2;         // cutout height

z_body = 30;                       // depth/height of the body

x_bcon     = w4;
y_bcon     = 2*w4;
z_bcon     = z_body/3;             // base-connector
z_bcon_off = z_body/3;

x_cable = 10;                      // cable-hole
z_cable = 10;
