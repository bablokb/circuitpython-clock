// -----------------------------------------------------------------------------
// 3D-Model (OpenSCAD) for a Badger2040.
//
// This model is the bottom support.
//
// Author: Bernhard Bablok
// License: GPL3
//
// https://github.com/bablokb/circuitpython-clock
//
// -----------------------------------------------------------------------------

include <dimensions.scad>
include <BOSL2/std.scad>

y_corpus_bot   = y1_panel/3;
y_corpus_top   = y_corpus_bot*2/3;
y_corpus_shift = (y_corpus_bot-y_corpus_top)/2;
h_corpus       = z_body + 20;


t_corpus = y_corpus_bot-2*w4 - (y_corpus_top-2*w4);
alpha = atan(t_corpus/h_corpus);                       // angle of corpus

// --- the corpus   ------------------------------------------------------------

module corpus() {
  rect_tube(size1=[x1_panel,y_corpus_bot],size2=[x1_panel,y_corpus_top],
                   h=h_corpus,wall=w4,shift=[0,-y_corpus_shift],
                   rounding=r_panel,irounding=r_panel,anchor=BOTTOM+CENTER);
}

// --- cutouts   -------------------------------------------------------------

module cutouts() {
  y_off_corpus = -(y_corpus_bot/2-w4/2)-fuzz;
  // cable hole
  translate([+1.5*x_cable,y_off_corpus,(z_body-z_cable)/2])
       cuboid([x_cable,w4+2*fuzz,z_cable],anchor=BOTTOM+CENTER);

  // lipo-pro
  translate([0,y_corpus_bot/2-w4-(h_corpus-y_holder)*t_corpus/h_corpus,h_corpus-y_holder])
                 xrot(alpha) cuboid([x_holder+2*gap,w4,y_holder+4*gap],anchor=BOTTOM+CENTER);

  // base-connector
  translate([-x1_panel/2+x1_panel/8,y_off_corpus,z_bcon_off])
       cuboid([x_bcon+gap/2,y_bcon+2*fuzz,z_bcon],anchor=BOTTOM+CENTER);
  translate([+x1_panel/2-x1_panel/8,y_off_corpus,z_bcon_off])
       cuboid([x_bcon+gap/2,y_bcon+2*fuzz,z_bcon],anchor=BOTTOM+CENTER);
}

// --- final model   ---------------------------------------------------------

module support() {
  difference() {
    corpus();
    cutouts();
  }
}

support();
