"""Inventory for computer builds"""

from app.utils.validators import validate_integer

class Resource:
    """Base class for resources"""
    def __init__(self, name, manufacturer, total, allocated):
        """Base class for builds

        Args:
            name (str): display name for resource
            manufacturer (str): resource manufacturer
            total (int): current inventory total
            allocated (int): number of resources in use

        Note:
            `allocated` cannot exceed `total`
        """
        self._name = name
        self._manufacturer = manufacturer

        validate_integer('total', total, 0)
        self._total = total
        validate_integer(
            'allocated', allocated, 0, total,
            custom_max_message='Allocated inventory cannot exceed total inventory.'
        )
        self._allocated = allocated

    @property
    def name(self):
        """

        Returns: 
            str: the resource name
        """
        return self._name

    @property
    def manufacturer(self):
        """

        Returns: 
            str: the manufacturer name
        """
        return self._manufacturer

    @property
    def total(self):
        """
        
        Returns: 
            int: the total inventory count
        """
        return self._total

    @property
    def allocated(self):
        """
        
        Returns: 
            int: the allocated inventory count
        """
        return self._allocated

    @property
    def category(self):
        """

        Returns:
            str: the resource category
        """
        return type(self).__name__.lower()

    @property
    def available(self):
        """

        Returns:
            int: the number of available resources
        """
        return self.total - self.allocated

    def __str__(self):
        return self.name

    def __repr__(self):
        return (f'{self.name} ({self.category} - {self.manufacturer}) : ' 
        f'total = {self.total}, allocated = {self.allocated}')
    
    def claim(self, n):
        """Claim a number of items

        Args:
            n (int): number of items in inventory to claim
        """
        validate_integer(
            'n', n, 1, self.available,
            custom_max_message='Cannot claim more than available (available = {self.available})'
        )
        self._allocated += n
    
    def freeup(self, n):
        """Return an inventory item to the available pool

        Args:
            n (int): number of items to return to available pool (cannot exceed
                     number of allocated items in inventory.)
        """
        validate_integer(
            'n', n, 1, self.allocated,
            custom_max_message='Cannot freeup more than allocated (allocated = {self.allocated})'
        )
        self._allocated -= n

    def died(self, n):
        """Return and permanently remove inventory from the pool.

        Args:
            n (int): number of items to remove from pool (cannot exceed number
                     allocated)
        """
        validate_integer(
            'n', n, 1, self._allocated,
            custom_max_message='Cannot retire more than allocated (allocated = {self.allocated})'
        )
        self._allocated -= n
        self._total -= n

    def purchased(self, n):
        """Add to inventory

        Args:
            n (int): number of items to add to inventory
        """
        validate_integer(
            'n', n, 1,
            custom_min_message='Must add at least one item.'
        )
        self._total += n


class CPU(Resource):
    """Resource subclass used to track CPU inventory pools"""

    def __init__(
            self, name, manufacturer, total, allocated,
            cores, socket, power_watts
    ):
        """

        Args:
            name (str): display name for resource
            manufacturer (str): resource manufacturer
            total (int): current inventory total
            allocated (int): number of resources in use
            cores (int): number of cores
            socket (str): socket type
            power_watts (int): power (in watts)
        """
        super().__init__(name, manufacturer, total, allocated)

        validate_integer('cores', cores, 1)
        validate_integer('power_watts', power_watts, 1)

        self._cores = cores
        self._socket = socket
        self._power_watts = power_watts

    @property
    def cores(self):
        """

        Returns:
            int: the number of cores
        """
        return self._cores

    @property
    def socket(self):
        """

        Returns:
            str: socket name
        """
        return self._socket

    @property
    def power_watts(self):
        """

        Returns:
            int: the power in watts
        """
        return self._power_watts

    def __repr__(self):
        return super().__repr__() + f', cores = {self.cores}, socket = {self.socket}, power_watts = {self.power_watts}'


class Storage(Resource):
    """A base class for storage devices"""
    def __init__(self, name, manufacturer, total, allocated, capacity_GB):
        """

        Args:
            name (str): display name for resource
            manufacturer (str): resource manufacturer
            total (int): current inventory total
            allocated (int): number of resources in use
            capacity_GB (int): storage capacity in GB
        """
        super().__init__(name, manufacturer, total, allocated)

        validate_integer('capacity_GB', capacity_GB, 1)
        self._capacity_GB = capacity_GB

    @property
    def capacity_GB(self):
        """

        Returns:
            int: the storage capacity 
        """
        return self._capacity_GB

    def __repr__(self):
        return f'{self.category}: {self.capacity_GB} GB'


class HDD(Storage):
    """HDD subclass"""
    def __init__(self, name, manufacturer, total, allocated, capacity_GB, size, rpm):
        """

        Args:
            name (str): display name for resource
            manufacturer (str): resource manufacturer
            total (int): current inventory total
            allocated (int): number of resources in use
            capacity_GB (int): storage capacity in GB
            size (str): indicates the device size (must be either 2.5" or 3.5")
            rpm (int): disk rotation speed (in rpm)
        """
        super().__init__(name, manufacturer, total, allocated, capacity_GB)

        allowed_sizes = ['2.5"', '3.5"']
        if size not in allowed_sizes:
            raise ValueError(f'Invalid HDD size. '
                             f'Must be one of {", ".join(allowed_sizes)}')
        validate_integer('rpm', rpm, min_value=1000, max_value=50000)

        self._size = size
        self._rpm = rpm

    
    @property
    def size(self):
        """
        
        Returns:
            str: the HDD size (2.5" / 3.5")
        """
        return self._size

    @property
    def rpm(self):
        """
        
        Returns:
            int: the HDD spin speed (rpm)
        """
        return self._rpm
    
    def __repr__(self):
        return super().__repr__() + f'({self.size}, {self.rpm} rpm)'

class SSD(Storage):
    """SSD subclass"""
    def __init__(self, name, manufacturer, total, allocated, capacity_GB, interface):
        """

        Args:
            name (str): display name for resource
            manufacturer (str): resource manufacturer
            total (int): current inventory total
            allocated (int): number of resources in use
            capacity_GB (int): storage capacity in GB
            interface (str): device interface (e.g. PCIe NVMe 3.0 x4)
        """
        super().__init__(name, manufacturer, total, allocated, capacity_GB)

        self._interface = interface

    @property
    def interface(self):
        """
        
        Returns:
            str: interface used by SSD
        """
        return self._interface

    def __repr__(self):
        s = super().__repr__()
        return f'{s} ({self.interface})'