# Copyright 2022 @RoadBalance
# Reference from https://pab47.github.io/legs.html
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sympy as sy


def func(x, y):
    return sy.Matrix([x**2 + y**2, 2*x + 3*y + 5])


x, y = sy.symbols('x y', real=True)
f = func(x, y)

J = sy.Matrix([
    sy.diff(f[0], x), sy.diff(f[0], y),
    sy.diff(f[1], x), sy.diff(f[1], y)
]).reshape(2, 2)

z = sy.Matrix([x, y])
J = f.jacobian(z)
print(J)

# (1, 2)
# J_sym = J.subs([x, 1], [y, 2])
# or
J_sym = J.subs([(x, 1), (y, 2)])
print(J_sym)
