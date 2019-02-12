#include <iostream>

#include "my_enums.h"
#include "generated/my_enums.gen.h"

using MyEnums::Color;
using MyEnums::Directions;

int main() {
    std::cout << enum_info<Color>::name(Color::Red) << '\n';
    std::cout << enum_info<Color>::name(Color::Green) << '\n';
    std::cout << enum_info<Color>::name(Color::Blue) << '\n';

    std::cout << enum_info<Directions>::name(Directions::Up) << '\n';
    std::cout << enum_info<Directions>::name(Directions::Down) << '\n';
    std::cout << enum_info<Directions>::name(Directions::Left) << '\n';
    std::cout << enum_info<Directions>::name(Directions::Right) << '\n';
    return 0;
}
