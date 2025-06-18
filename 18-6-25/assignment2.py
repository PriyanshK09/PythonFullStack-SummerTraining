import math

class Vector3D:
    def __init__(self, x, y, z):
        """Initialize the vector with three components: x, y, and z."""
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        """Return a readable string representation of the vector."""
        return f"Vector3D({self.x}, {self.y}, {self.z})"
    
    def __repr__(self):
        """Return a detailed string representation of the vector."""
        return f"Vector3D(x={self.x}, y={self.y}, z={self.z})"
    
    def __eq__(self, other):
        """Check equality of two vectors (component-wise)."""
        if not isinstance(other, Vector3D):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __add__(self, other):
        """Vector addition."""
        if not isinstance(other, Vector3D):
            raise TypeError("Can only add Vector3D to Vector3D")
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, other):
        """Scalar multiplication or dot product."""
        if isinstance(other, (int, float)):
            # Scalar multiplication
            return Vector3D(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector3D):
            # Dot product
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise TypeError("Can only multiply by scalar or Vector3D")
    
    def __rmul__(self, other):
        """Right multiplication for scalar * vector."""
        return self.__mul__(other)
    
    def magnitude(self):
        """Return the Euclidean norm (length) of the vector."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def __lt__(self, other):
        """Less than comparison based on magnitude."""
        if not isinstance(other, Vector3D):
            raise TypeError("Can only compare Vector3D with Vector3D")
        return self.magnitude() < other.magnitude()
    
    def __le__(self, other):
        """Less than or equal comparison based on magnitude."""
        if not isinstance(other, Vector3D):
            raise TypeError("Can only compare Vector3D with Vector3D")
        return self.magnitude() <= other.magnitude()
    
    def __gt__(self, other):
        """Greater than comparison based on magnitude."""
        if not isinstance(other, Vector3D):
            raise TypeError("Can only compare Vector3D with Vector3D")
        return self.magnitude() > other.magnitude()
    
    def __ge__(self, other):
        """Greater than or equal comparison based on magnitude."""
        if not isinstance(other, Vector3D):
            raise TypeError("Can only compare Vector3D with Vector3D")
        return self.magnitude() >= other.magnitude()
    
    def __getitem__(self, index):
        """Enable access to components via index ([0], [1], [2])."""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Vector3D index out of range (0-2)")
    
    def cross(self, other):
        """Return the cross product of two 3D vectors."""
        if not isinstance(other, Vector3D):
            raise TypeError("Cross product requires another Vector3D")
        
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        
        return Vector3D(x, y, z)
    
    @staticmethod
    def zero():
        """Return a zero vector (0, 0, 0)."""
        return Vector3D(0, 0, 0)


# Example usage and testing
if __name__ == "__main__":
    # Create vectors
    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)
    
    print("Vector 1:", v1)
    print("Vector 2:", v2)
    print()
    
    # Vector addition
    print("v1 + v2 =", v1 + v2)
    
    # Dot product
    print("v1 * v2 (dot product) =", v1 * v2)
    
    # Scalar multiplication
    print("v1 * 2 =", v1 * 2)
    print("3 * v1 =", 3 * v1)
    
    # Cross product
    print("v1.cross(v2) =", v1.cross(v2))
    
    # Equality
    print("v1 == v2:", v1 == v2)
    print("v1 == Vector3D(1, 2, 3):", v1 == Vector3D(1, 2, 3))
    
    # Magnitude comparison
    print("v1 < v2:", v1 < v2)
    print("v1.magnitude() =", v1.magnitude())
    print("v2.magnitude() =", v2.magnitude())
    
    # Indexing
    print("v1[0], v1[1], v1[2] =", v1[0], v1[1], v1[2])
    
    # Zero vector
    print("Zero vector:", Vector3D.zero())