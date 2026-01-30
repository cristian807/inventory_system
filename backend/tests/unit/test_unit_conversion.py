import pytest


class TestUnitConversionFormula:
    def test_basic_unit_conversion(self):
        packages_count = 10
        units_per_package = 12
        
        calculated_quantity = packages_count * units_per_package
        
        assert calculated_quantity == 120, \
            f"10 cajas de 12 unidades debería dar 120, obtuvo {calculated_quantity}"
    
    
    def test_single_unit_products(self):
        packages_count = 25  # 25 artículos individuales
        units_per_package = 1  # 1 unidad por "empaque"
        
        calculated_quantity = packages_count * units_per_package
        
        assert calculated_quantity == 25, \
            f"25 unidades individuales debería dar 25, obtuvo {calculated_quantity}"
    
    
    def test_large_packages_pallets(self):
        packages_count = 5  # 5 pallets
        units_per_package = 240  # 240 botellas por pallet
        
        calculated_quantity = packages_count * units_per_package
        
        assert calculated_quantity == 1200, \
            f"5 pallets de 240 unidades debería dar 1200, obtuvo {calculated_quantity}"
    
    
    def test_medium_packages(self):
        packages_count = 100  # 100 paquetes
        units_per_package = 6  # 6 latas por paquete
        
        calculated_quantity = packages_count * units_per_package
        
        assert calculated_quantity == 600, \
            f"100 paquetes de 6 unidades debería dar 600, obtuvo {calculated_quantity}"
    
    
    def test_zero_packages(self):
        packages_count = 0
        units_per_package = 12
        
        calculated_quantity = packages_count * units_per_package
        
        assert calculated_quantity == 0, \
            f"0 empaques debería dar 0 unidades, obtuvo {calculated_quantity}"
    
    
    def test_accumulation_logic(self):
        """
        Prueba lógica de acumulación: agregar 10 cajas cuando ya existen 5
        
        Escenario:
        - Inventario inicial: 5 cajas × 12 = 60 unidades
        - Nuevo conteo: 10 cajas × 12 = 120 unidades
        - Total acumulado: 60 + 120 = 180 unidades
        """
        # Inventario inicial
        existing_packages = 5
        units_per_package = 12
        existing_quantity = existing_packages * units_per_package
        assert existing_quantity == 60
        
        # Nuevas cajas agregadas
        new_packages = 10
        new_quantity = new_packages * units_per_package
        assert new_quantity == 120
        
        # Total acumulado
        total_quantity = existing_quantity + new_quantity
        assert total_quantity == 180, \
            f"60 unidades iniciales + 120 nuevas debería dar 180, obtuvo {total_quantity}"
    
    

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
