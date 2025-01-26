module RoundedCornerSquareBase() {
    minkowski() {
        // the square base
        translate([0, 0, baseHeight / 2]) {
            color("blue")
            cube([baseWidth, baseLength, baseHeight], center=true);
        }

        // create rounded corners
        cylinder(r=5, h=1);
    }

    CoffeeShopName();
}
