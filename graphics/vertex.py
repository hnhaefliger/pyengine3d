import math

class Vertex:
    def __init__(self, point):
        #store x, y, z coordinates
        (x,y,z) = point
        self.x = x
        self.y = y
        self.z = z

    def flatten(self, scale, distance):
        #calculate 2D coordinates from 3D point
        projectedY = int(((self.y * distance) / (self.z + distance)) * scale)
        projectedX = int(((self.x * distance) / (self.z + distance)) * scale)
        return (projectedX, projectedY)

    def rotate(self, axis, angle):
        #rotate point around axis
        angle = angle / 450 * 180 / math.pi
        #sqrt2 = math.sqrt(2)
        if axis == 'z':
            #rotate aroud Z axis
            newX = self.x * math.cos(angle) - self.y * math.sin(angle)
            newY = self.y * math.cos(angle) + self.x * math.sin(angle)
            newZ = self.z
        elif axis == 'x':
            #rotate around X axis
            newY = self.y * math.cos(angle) - self.z * math.sin(angle)
            newZ = self.z * math.cos(angle) + self.y * math.sin(angle)
            newX = self.x
        elif axis == 'y':
            #rotate around Y axis
            newX = self.x * math.cos(angle) - self.z * math.sin(angle)
            newZ = self.z * math.cos(angle) + self.x * math.sin(angle)
            newY = self.y
        else:
            raise ValueError('invalid rotation axis')
        self.x = newX
        self.y = newY
        self.z = newZ

    def move(self, axis, value):
        if axis == 'x':
            self.x += value
        elif axis == 'y':
            self.y += value
        elif axis == 'z':
            self.z += value
        else:
            raise ValueError('Invalid movement axis')

    def free_rotate(self, phi, A, B):
        """Compute new coordinates for self as image of itself by the rotation R
        of phi degrees around the AB vector."""
        # Define conjugate and * for Quaternions (4-tuples)
        class Quaternion(tuple):
            def conj(self):
                return self[0], *[-self[i] for i in range(1,4)]
            def __mul__(self, q2):
                w1, x1, y1, z1 = self
                w2, x2, y2, z2 = q2
                w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
                x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
                y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
                z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
                return w, x, y, z
        # Compute "vector to rotate" quaternion using vector Aself.
        p = Quaternion((0, self.x-A.x, self.y-A.y, self.z-A.z))
        # Compute "rotation" quaternion using vector of AB.
        ABx, ABy, ABz = B.x-A.x, B.y-A.y, B.z-A.z
        nAB = math.sqrt(ABx**2 + ABy**2 + ABz**2)
        half_phi_rad = phi / 360 * math.pi
        S = math.sin(half_phi_rad)
        r = Quaternion((math.cos(half_phi_rad), S*ABx/nAB, S*ABy/nAB, S*ABz/nAB))
        # Calculate "image" quaternion using p and r conjugation (q = r⋅p⋅r^-1).
        qw, qx, qy, qz = Quaternion(r * p) * r.conj()
        # Get Q coordinates.
        self.x, self.y, self.z = qx+A.x, qy+A.y, qz+A.z
