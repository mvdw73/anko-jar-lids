//diameter of container neck
d=53.6; //.1
//thread pitch
p=4.0; //.1
//thread height
h=1.1; //.01
//thread width
w=2.36; //.01
//thread turns
tr=1.05; //.01
//number of threads
nt=1;
//cap depth (inner)
cd=11.3; //.1
//thread start (from bottom of cap to bottom of thread)
ts=1.3; //.1
//cap thickness
th=2.5; //.1
//number of ridges
rdg=48;
//clearance
cl=.2; //.01

module __Customizer_Limit__ () {}  // Hide following assignments from Customizer.
f=100;
$fn=f;
//neck radius
r=d/2;

mcm=0.001;


//thread profile (a slice across 1 thread)
profile=[[0,r+h+cl],[w/3,r+cl],[w*2/3,r+cl],[w,r+h+cl],[p,r+h+cl]];

//profile scaled to 360°
scaledProfile=[for (i=[0:1/f:1-1/f]) [i*360,lookup(i*p,profile)]];
//number of turns represented by the width
t2=w/p;

//cross section of thread
module crossSection()
{
  //profile wrapped around a perimeter
  pts=[for (sp=scaledProfile) [-sp[1]*cos(sp[0]),sp[1]*sin(sp[0])]];
  //the resulting polygon representing a horizontal slice through the thread
  difference()
  {
    circle(r=r+h+cl+th/2); 
    polygon(pts);
  }
}

//thread
module thread()
{
  translate([0,0,cd+th-p*(tr+t2)-ts])
  union()
  {
    difference()
    {
      //create thread and outer shell
      rotate([0,0,-t2*360])
      mirror([1,0,0])
      linear_extrude(p*(tr+t2),twist=(tr+t2)*360,convexity=5)
      crossSection();
      //blunt top end
      rotate([0,0,tr*360])
      rotate_extrude(angle=t2*360)
      translate([0,p*tr-mcm])
      square([r+h+cl,w+mcm*2]);
      //blunt bottom end
      rotate_extrude(angle=-t2*360)
      translate([0,-mcm])
      square([r+h+cl,w+mcm*2]);
    }
    //rounded ends of the thread
    intersection()
    {
      cylinder(h=p*(tr+t2),r=r+h+cl+th/2);
      union()
      {
        translate([r+h+cl,0,0])
        rotate_extrude()
        polygon([[0,0],[h,w/3],[h,w*2/3],[0,w]]);
        rotate([0,0,tr*360])
        translate([r+h+cl,0,p*tr])
        rotate_extrude()
        polygon([[0,0],[h,w/3],[h,w*2/3],[0,w]]);
      }
    }
  }
}

//the main structure of the cap
module capBody()
{
  rotate_extrude()
  polygon([[0,0],[r+h+cl+th/2,0],[r+h+cl+th,th/2],[r+h+cl+th,cd+th],[r+h+cl,cd+th],[r+h+cl,th],[0,th]
  ]);
}

//external ridges on the cap
module ridges()
{
  if(rdg>0)
  {
    //ridges
    for(ridge=[0:rdg-1])
    {
      hull()
      {
        rotate([0,0,360/rdg*ridge])
        translate([r+h+cl+th,0,th*5/4])
        sphere(r=th/4);
        rotate([0,0,360/rdg*ridge])
        translate([r+h+cl+th,0,cd+th/2])
        sphere(r=th/4);
      }
    }
  }
}

//all together: cap, thread(s), ridges
union()
{
  capBody();
  for(a=[0:360/nt:360-(360/nt)])
  {
    rotate([0,0,a])
    thread();
  }
  ridges();
}


