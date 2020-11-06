import unittest

class ProductoInexistente(Exception):
    pass

class PrecioProductoNoDefinido(Exception):
    pass

class CompraNoFinalizada(Exception):
    pass

class CompraYaFinalizada(Exception):
    pass

class CompraVacía(Exception):
    pass

class PagoInsuficiente(Exception):
    pass

class Producto(object):
    
    def __init__(self, codigo):
        self._codigo = codigo
        
    def codigo(self):
        return self._codigo

class ListaDePrecios(object):

    def __init__(self):
        self.precio_de_los_productos = {}
        self.descuento_de_los_productos = {}

    def precio_de(self, un_producto):
        if not un_producto in self.precio_de_los_productos.keys():
            raise PrecioProductoNoDefinido("El precio del producto {} no esta definido.".format(un_producto.codigo()))
        return self.precio_de_los_productos[un_producto]

    def precio_descuento_de(self, un_producto):
        if not un_producto in self.precio_de_los_productos.keys():
            raise PrecioProductoNoDefinido("El precio del producto {} no esta definido.".format(un_producto.codigo()))
        precio_del_producto = self.precio_de_los_productos[un_producto]
        descuento_del_producto = self.descuento_de_los_productos.get(un_producto, 0)
        return  precio_del_producto - (precio_del_producto* descuento_del_producto)

    def establecer_precio_para(self, un_producto, valor_precio):
        self.precio_de_los_productos[un_producto] = valor_precio

    def establecer_descuento_para(self, un_producto, un_porcentaje):
        self.descuento_de_los_productos[un_producto] = un_porcentaje

class Compra(object):
    
    def __init__(self):
        self._productos = []
        self.finalizado = False

    def productos(self):
        return self._productos

    def agregar_producto(self, un_producto):
        self._productos.append(un_producto)

    def finalizar(self):
        if self.finalizado:
            raise CompraYaFinalizada("La compra ya se encuentra finalizada")
        if not self._productos:
            raise CompraVacía("La compra no tiene productos")
        self.finalizado = True

class CajaRegistradora(object):
    
    def __init__(self, lista_producto, una_lista_de_precios):
        self.lista_de_productos = lista_producto
        self.price_list = una_lista_de_precios
        self._compra_actual = Compra()

    def escanear_producto(self, codigo_producto):
        
        productos_seleccionados = filter(lambda p: p.codigo() == codigo_producto, self.lista_de_productos)
        if not productos_seleccionados:
            raise ProductoInexistente("El producto con código {} no existe".format(codigo_producto))
        return productos_seleccionados[0]

    def agregar_producto(self, codigo_producto):
        un_producto = self.escanear_producto(codigo_producto)
        self.compra_actual().agregar_producto(un_producto)

    def compra_actual(self):
        return self._compra_actual

    def subtotal(self):
        subtotal = 0
        for product in self.compra_actual().productos():
            subtotal += self.price_list.precio_de(product)
        return subtotal

    def finalizar_compra(self):
        self.compra_actual().finalizar()

    def total(self):
        if not self.compra_actual().finalizado:
            raise CompraNoFinalizada("Compra no finalizada.")
        total = 0
        for product in self.compra_actual().productos():
            total += self.price_list.discounted_precio_de(product)
        return total

    def pagar_compra_con(self, cantidad_de_dinero):
        total = self.total()
        if total > cantidad_de_dinero:
            raise PagoInsuficiente("El pago debe ser mayor al total de la compra.")
        return cantidad_de_dinero - self.total()

class CajaRegistradoraTest(unittest.TestCase):

    def setUp(self):
        un_producto = Producto('1002A')
        otro_producto = Producto('1003A')
        producto_sin_precio = Producto('1004A')
        self.lista_de_productos = [un_producto, otro_producto, producto_sin_precio]

        self.lista_de_precios = ListaDePrecios()
        self.lista_de_precios.establecer_precio_para(un_producto, 10.00)
        self.lista_de_precios.establecer_precio_para(otro_producto, 5.00)

        self.caja_registradora = CajaRegistradora(lista_producto=self.lista_de_productos, una_lista_de_precios=self.lista_de_precios)

    def test_01_agregar_producto_no_existente(self):
        caja_registradora = CajaRegistradora(lista_producto=[], una_lista_de_precios=ListaDePrecios())
        codigo_producto = '1001A'
        
        self.assertRaises(ProductoInexistente, caja_registradora.agregar_producto, codigo_producto)

    def test_02_agregar_producto_existente(self):
        codigo_producto = '1002A'
        un_producto = self.caja_registradora.agregar_producto(codigo_producto)

        self.assertEqual(1, len(self.caja_registradora.compra_actual().productos()))
        self.assertEqual('1002A', self.caja_registradora.compra_actual().productos()[0].codigo())

    def test_03_subtotal_sin_productos(self):
        caja_registradora = CajaRegistradora(lista_producto=[], una_lista_de_precios=ListaDePrecios())
        self.assertEqual(0, caja_registradora.subtotal())

    def test_04_subtotal_productos_sin_precios(self):
        codigo_producto = '1004A'
        un_producto = self.caja_registradora.agregar_producto(codigo_producto)

        self.assertRaises(PrecioProductoNoDefinido, self.caja_registradora.subtotal)

    def test_05_subtotal_con_un_producto(self):
        codigo_producto = '1002A'
        un_producto = self.caja_registradora.agregar_producto(codigo_producto)
        
        self.assertEqual(10.00, self.caja_registradora.subtotal())

    def test_06_subtotal_con_dos_productos(self):
        codigo_producto = '1002A'
        self.caja_registradora.agregar_producto(codigo_producto)

        otro_codigo_producto = '1003A'
        self.caja_registradora.agregar_producto(otro_codigo_producto)

        self.assertEqual(15.00, self.caja_registradora.subtotal())

    def test_07_total_sin_finalizar_compra(self):
        codigo_producto = '1002A'
        un_producto = self.caja_registradora.agregar_producto(codigo_producto)

        self.assertRaises(CompraNoFinalizada, self.caja_registradora.total)

    def test_08_finalizar_compra_vacía(self):
        self.assertRaises(CompraVacía, self.caja_registradora.finalizar_compra)

    def test_09_finalizar_compra_ya_finalizada(self):
        codigo_producto = '1002A'
        un_producto = self.caja_registradora.agregar_producto(codigo_producto)

        self.caja_registradora.finalizar_compra()

        self.assertRaises(CompraYaFinalizada, self.caja_registradora.finalizar_compra)

    def test_10_total_un_producto_sin_descuento(self):
        codigo_producto = '1002A'
        un_producto = self.caja_registradora.agregar_producto(codigo_producto)

        self.caja_registradora.finalizar_compra()

        self.assertEqual(10.00, self.caja_registradora.total())

    def test_11_total_dos_productos_sin_descuento(self):
        codigo_producto = '1002A'
        un_producto = self.caja_registradora.agregar_producto(codigo_producto)

        otro_codigo_producto = '1003A'
        self.caja_registradora.agregar_producto(otro_codigo_producto)

        self.caja_registradora.finalizar_compra()

        self.assertEqual(15.00, self.caja_registradora.total())

    def test_12_total_un_producto_sin_descuento(self):
        codigo_producto = '1002A'
        un_producto = filter(lambda p: p.codigo() == codigo_producto, self.lista_de_productos)[0]

        lista_de_precios = ListaDePrecios()
        lista_de_precios.establecer_precio_para(un_producto, 10.00)
        lista_de_precios.establecer_descuento_para(un_producto, 0.1)
        
        caja_registradora = CajaRegistradora(lista_producto=self.lista_de_productos, una_lista_de_precios=lista_de_precios)
        un_producto = caja_registradora.agregar_producto(codigo_producto)

        caja_registradora.finalizar_compra()

        self.assertEqual(9.00, caja_registradora.total())

    def test_13_pagar_compra_sin_dinero_suficiente(self):
        codigo_producto = '1002A'
        un_producto = self.caja_registradora.agregar_producto(codigo_producto)

        otro_codigo_producto = '1003A'
        self.caja_registradora.agregar_producto(otro_codigo_producto)

        self.caja_registradora.finalizar_compra()

        self.assertEqual(15.00, self.caja_registradora.total())

        self.assertRaises(PagoInsuficiente, self.caja_registradora.pagar_compra_con, 13.00)

    def test_14_pagar_compra_sin_cambios(self):
        codigo_producto = '1002A'
        un_producto = self.caja_registradora.agregar_producto(codigo_producto)

        otro_codigo_producto = '1003A'
        self.caja_registradora.agregar_producto(otro_codigo_producto)

        self.caja_registradora.finalizar_compra()

        self.assertEqual(15.00, self.caja_registradora.total())

        self.assertEqual(0.00, self.caja_registradora.pagar_compra_con(15.00))

    def test_15_pagar_compra_con_cambios(self):
        codigo_producto = '1002A'
        un_producto = self.caja_registradora.agregar_producto(codigo_producto)

        otro_codigo_producto = '1003A'
        self.caja_registradora.agregar_producto(otro_codigo_producto)

        self.caja_registradora.finalizar_compra()

        self.assertEqual(15.00, self.caja_registradora.total())

        self.assertEqual(5.00, self.caja_registradora.pagar_compra_con(20.00))

if __name__ == '__main__':
    unittest.main()