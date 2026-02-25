import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { motionTokens } from '../../utils/motionTokens';
import { productosAPI } from '../../services/api';
import Card from '../../components/Card';
import Button from '../../components/Button';
import './ProductosList.css';

const ProductosList = () => {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProductos();
  }, []);

  const fetchProductos = async () => {
    try {
      setLoading(true);
      const response = await productosAPI.getAll();
      if (response.data.success) {
        setProductos(response.data.data);
      }
    } catch (err) {
      setError('Error al cargar productos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar este producto?')) {
      try {
        await productosAPI.delete(id);
        fetchProductos();
      } catch (err) {
        alert('Error al eliminar producto');
      }
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: motionTokens.stagger
      }
    }
  };

  const itemVariants = {
    hidden: { x: 24, opacity: 0 },
    visible: {
      x: 0,
      opacity: 1,
      transition: { duration: motionTokens.durationBase, ease: motionTokens.ease }
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <motion.div
          className="loading-spinner"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
        <p>Cargando productos...</p>
      </div>
    );
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="productos-page">
      <div className="page-header">
        <motion.h1
          initial={{ opacity: 0, x: -36 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: motionTokens.durationBase, ease: motionTokens.ease }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="page-icon">
            <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
          </svg>
          Productos
        </motion.h1>
        <Button onClick={() => navigate('/productos/crear')}>
          + Nuevo Producto
        </Button>
      </div>

      <motion.div
        className="productos-grid"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {productos.map((producto, index) => (
            <motion.div key={producto.id} variants={itemVariants}>
            <Card delay={index * 0.05}>
              <div className="producto-card">
                <div className="producto-header">
                  <h3>{producto.nombre}</h3>
                  {producto.necesita_reabastecimiento && (
                    <span className="badge badge-warning">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="badge-icon">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                      </svg>
                      Bajo Stock
                    </span>
                  )}
                </div>
                
                <div className="producto-info">
                  <p><strong>Categoría:</strong> {producto.categoria_nombre}</p>
                  <p><strong>Proveedor:</strong> {producto.proveedor_nombre}</p>
                  <p><strong>Precio:</strong> ${parseFloat(producto.precio).toFixed(2)}</p>
                  <p>
                    <strong>Stock:</strong> 
                    <span className={producto.stock < producto.stock_minimo ? 'stock-bajo' : 'stock-ok'}>
                      {producto.stock} / {producto.stock_minimo}
                    </span>
                  </p>
                </div>

                {producto.descripcion && (
                  <p className="producto-descripcion">{producto.descripcion}</p>
                )}

                <div className="card-actions">
                  <Button 
                    variant="secondary" 
                    size="small"
                    onClick={() => navigate(`/productos/${producto.id}`)}
                  >
                    Ver Detalles
                  </Button>
                  <Button 
                    variant="outline" 
                    size="small"
                    onClick={() => navigate(`/productos/editar/${producto.id}`)}
                  >
                    Editar
                  </Button>
                  <Button 
                    variant="danger" 
                    size="small"
                    onClick={() => handleDelete(producto.id)}
                  >
                    Eliminar
                  </Button>
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </motion.div>

      {productos.length === 0 && (
        <motion.div
          className="empty-state"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <h2>No hay productos registrados</h2>
          <p>Comienza agregando tu primer producto</p>
          <Button onClick={() => navigate('/productos/crear')}>
            + Crear Producto
          </Button>
        </motion.div>
      )}
    </div>
  );
};

export default ProductosList;
