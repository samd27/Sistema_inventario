import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { motionTokens } from '../../utils/motionTokens';
import { productosAPI, categoriasAPI, proveedoresAPI } from '../../services/api';
import Card from '../../components/Card';
import Button from '../../components/Button';
import './ProductosList.css';

const emptyForm = {
  nombre: '',
  descripcion: '',
  precio: '',
  stock: '',
  stock_minimo: '',
  categoria_id: '',
  proveedor_id: ''
};

const ProductosList = () => {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [proveedores, setProveedores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [detailId, setDetailId] = useState(null);
  const [formData, setFormData] = useState(emptyForm);

  useEffect(() => {
    fetchProductos();
    fetchCategorias();
    fetchProveedores();
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

  const fetchCategorias = async () => {
    try {
      const response = await categoriasAPI.getAll();
      if (response.data.success) setCategorias(response.data.data);
    } catch (err) {
      console.error('Error al cargar categorías', err);
    }
  };

  const fetchProveedores = async () => {
    try {
      const response = await proveedoresAPI.getAll();
      if (response.data.success) setProveedores(response.data.data);
    } catch (err) {
      console.error('Error al cargar proveedores', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        precio: parseFloat(formData.precio),
        stock: parseInt(formData.stock),
        stock_minimo: parseInt(formData.stock_minimo),
        categoria_id: parseInt(formData.categoria_id),
        proveedor_id: parseInt(formData.proveedor_id)
      };
      if (editingId) {
        await productosAPI.update(editingId, payload);
      } else {
        await productosAPI.create(payload);
      }
      handleCancel();
      fetchProductos();
    } catch (err) {
      alert('Error al guardar producto');
      console.error(err);
    }
  };

  const handleEdit = (producto) => {
    setEditingId(producto.id);
    setDetailId(null);
    setFormData({
      nombre: producto.nombre,
      descripcion: producto.descripcion || '',
      precio: producto.precio,
      stock: producto.stock,
      stock_minimo: producto.stock_minimo,
      categoria_id: producto.categoria_id,
      proveedor_id: producto.proveedor_id
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar este producto?')) {
      try {
        await productosAPI.delete(id);
        if (detailId === id) setDetailId(null);
        fetchProductos();
      } catch (err) {
        alert('Error al eliminar producto');
      }
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingId(null);
    setFormData(emptyForm);
  };

  const handleNewClick = () => {
    setDetailId(null);
    setEditingId(null);
    setFormData(emptyForm);
    setShowForm(!showForm);
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

  const detailProducto = detailId ? productos.find(p => p.id === detailId) : null;

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
        <Button onClick={handleNewClick}>
          {showForm && !editingId ? 'Cancelar' : '+ Nuevo Producto'}
        </Button>
      </div>

      {/* Formulario de crear / editar */}
      {showForm && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card className="form-card">
            <h2>{editingId ? 'Editar Producto' : 'Nuevo Producto'}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-row">
                <div className="form-group">
                  <label>Nombre *</label>
                  <input
                    type="text"
                    value={formData.nombre}
                    onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Precio *</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={formData.precio}
                    onChange={(e) => setFormData({ ...formData, precio: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Descripción</label>
                <textarea
                  value={formData.descripcion}
                  onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
                  rows="2"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Stock *</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.stock}
                    onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Stock Mínimo *</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.stock_minimo}
                    onChange={(e) => setFormData({ ...formData, stock_minimo: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Categoría *</label>
                  <select
                    value={formData.categoria_id}
                    onChange={(e) => setFormData({ ...formData, categoria_id: e.target.value })}
                    required
                  >
                    <option value="">-- Seleccionar --</option>
                    {categorias.map(c => (
                      <option key={c.id} value={c.id}>{c.nombre}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Proveedor *</label>
                  <select
                    value={formData.proveedor_id}
                    onChange={(e) => setFormData({ ...formData, proveedor_id: e.target.value })}
                    required
                  >
                    <option value="">-- Seleccionar --</option>
                    {proveedores.map(p => (
                      <option key={p.id} value={p.id}>{p.nombre}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-actions">
                <Button type="submit" variant="success">
                  {editingId ? 'Actualizar' : 'Crear'}
                </Button>
                <Button type="button" variant="outline" onClick={handleCancel}>
                  Cancelar
                </Button>
              </div>
            </form>
          </Card>
        </motion.div>
      )}

      {/* Detalle de producto */}
      {detailProducto && !showForm && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card className="form-card">
            <div className="detail-header">
              <h2>{detailProducto.nombre}</h2>
              <Button variant="outline" size="small" onClick={() => setDetailId(null)}>Cerrar</Button>
            </div>
            <div className="detail-grid">
              <p><strong>Descripción:</strong> {detailProducto.descripcion || 'Sin descripción'}</p>
              <p><strong>Precio:</strong> ${parseFloat(detailProducto.precio).toFixed(2)}</p>
              <p><strong>Stock:</strong> {detailProducto.stock} (mín: {detailProducto.stock_minimo})</p>
              <p><strong>Categoría:</strong> {detailProducto.categoria_nombre}</p>
              <p><strong>Proveedor:</strong> {detailProducto.proveedor_nombre}</p>
              {detailProducto.necesita_reabastecimiento && (
                <p className="stock-bajo"><strong>⚠ Necesita reabastecimiento</strong></p>
              )}
            </div>
          </Card>
        </motion.div>
      )}

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
                    <strong>Stock:</strong>{' '}
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
                    onClick={() => { setDetailId(producto.id); setShowForm(false); }}
                  >
                    Ver Detalles
                  </Button>
                  <Button 
                    variant="outline" 
                    size="small"
                    onClick={() => handleEdit(producto)}
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

      {productos.length === 0 && !showForm && (
        <motion.div
          className="empty-state"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <h2>No hay productos registrados</h2>
          <p>Comienza agregando tu primer producto</p>
          <Button onClick={handleNewClick}>
            + Crear Producto
          </Button>
        </motion.div>
      )}
    </div>
  );
};

export default ProductosList;
