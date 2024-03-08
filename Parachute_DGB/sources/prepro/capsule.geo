// This is the mesh size
cl_capsule = 0.1;
cl_shoulder = 0.025;
//The top circle of the capsule is centered at (0, y=ya), with radius -xa,
//Point (xa, ya) is on the top circle, modify it to change the size of the capsule. 
//xa = -0.31142370413265841
xa = -0.31142370413265841;
//The position of the capsule
//zshift = -4.7487995381941190e+01;
zshift = 0.0;
za = -8.895 + zshift;
xb = -xa;


x4 = 2.25;
x3 = x4 - 1.012*Tan(36.9*Pi/180);
x2 = x3 - 0.506*Tan(59*Pi/180);
x1 = x2 - 0.5*Tan(33.95*Pi/180);

z1 = 0;
z2 = -0.5;
z3 = -0.5-0.506;
z4 = -0.5-0.506-1.012;
o_x = 0.0;
o_z = z4 - 2.25*Tan(20*Pi/180) + 0.5* 2.25/Cos(20*Pi/180);
nose_x_a = o_x + 1.125*Cos(-70*Pi/180);
nose_z_a = o_z + 1.125*Sin(-70*Pi/180);
nose_x_b = o_x + 1.125*Cos(-110*Pi/180);
nose_z_b = o_z + 1.125*Sin(-110*Pi/180);

Printf("o_z before scale is %g", o_z);
Printf("nose_z_b before scale is %g", nose_z_b);

shoulder_r = 0.125;
shoulder_theta = 73.1;
shoulder_h = shoulder_r/Sin(shoulder_theta/2.0*Pi/180);
shoulder_l = shoulder_r/Tan(shoulder_theta/2.0*Pi/180);


scale = (xb - xa)/(2*x1);
Printf("scale is %g",scale);
x4 *= scale;
x3 *= scale;
x2 *= scale;
x1 *= scale;
z1 *= scale;
z2 *= scale;
z3 *= scale;
z4 *= scale;
o_x *= scale;
o_z *= scale;

nose_x_a *= scale;
nose_x_b *= scale;
nose_z_a *= scale;
nose_z_b *= scale;



Point(7) = {0 + xa + x1,0, 0 +za - z1,cl_capsule};
Point(8) = {x1 + xa + x1,0,z1 +za - z1,cl_capsule};
Point(9) = {x2 + xa + x1,0,z2 +za - z1,cl_capsule};
Point(10) = {x3 + xa + x1,0,z3 +za - z1,cl_capsule};
//right shoulder corner
Point(11) = {x4 + xa + x1 - shoulder_h*Cos((shoulder_theta/2.0 - 20.0)*Pi/180),0,z4 +za - z1 + shoulder_h*Sin((shoulder_theta/2.0 - 20.0)*Pi/180),cl_shoulder};
Point(12) = {x4 + xa + x1 - shoulder_l*Cos(53.1*Pi/180),0,z4 +za - z1 + shoulder_l*Sin(53.1*Pi/180),cl_shoulder};
Point(13) = {x4 + xa + x1 - shoulder_l*Cos(20.0*Pi/180),0,z4 +za - z1 - shoulder_l*Sin(20.0*Pi/180),cl_shoulder};

Point(14) = {o_x + xa + x1,0,o_z +za - z1,cl_capsule};
Point(15) = {nose_x_a + xa + x1,0,nose_z_a +za - z1,cl_capsule};

Point(16) = {o_x + xa + x1,0, o_z - 1.125 +za - z1,cl_capsule};


Printf("z_min is %g",nose_z_a +za - z1);

Printf("scale is %g", scale);

Printf("z_a - z_1 after scale is %g", za - z1);

Printf("o_z after scale is %g", o_z);

Printf("nose_z_b after scale is %g", nose_z_b);

//+
Line(1) = {7, 8};
//+
Line(2) = {8, 9};
//+
Line(3) = {9, 10};
//+
Line(4) = {10, 12};

//+
Circle(5) = {12, 11, 13};
//+
Line(6) = {13, 15};

//+
Circle(7) = {15, 14, 16};


//+
Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2} {
  Line{1, 2, 3, 4, 5, 6, 7};
}

Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2} {
  Line{8, 11, 15, 19, 23, 27, 31};
}

Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2} {
  Line{34, 37, 41, 45, 49, 53, 57};
}


Extrude {{0, 0, 1}, {0, 0, 0}, Pi/2} {
  Line{60, 63, 67, 71, 75, 79, 83};
}



Physical Surface("CapsuleSurface") = {88, 62, 36, 10, 66, 40, 14, 92, 70, 44, 18, 96, 100, 74, 48, 22, 78, 52, 26, 104, 108, 30, 56, 82, 111, 33, 59, 85};
