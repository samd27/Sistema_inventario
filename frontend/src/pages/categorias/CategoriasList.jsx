import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { motionTokens } from '../../utils/motionTokens';
import { categoriasAPI } from '../../services/api';
import Card from '../../components/Card';
import Button from '../../components/Button';
import './CategoriasList.css';

const CategoriasList = () => {
  const [categorias, setCategorias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({ nombre: '', descripcion: '' });

  useEffect(() => {
    fetchCategorias();
  }, []);

  const fetchCategorias = async () => {
    try {
      setLoading(true);
      const response = await categoriasAPI.getAll();
      if (response.data.success) {
        setCategorias(response.data.data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await categoriasAPI.update(editingId, formData);
      } else {
        await categoriasAPI.create(formData);
      }
      setShowForm(false);
      setEditingId(null);
      setFormData({ nombre: '', descripcion: '' });
      fetchCategorias();
    } catch (err) {
      alert('Error al guardar categoría');
    }
  };

  const handleEdit = (categoria) => {
    setEditingId(categoria.id);
    setFormData({ nombre: categoria.nombre, descripcion: categoria.descripcion });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de eliminar esta categoría?')) {
      try {
        await categoriasAPI.delete(id);
        fetchCategorias();
      } catch (err) {
        alert('Error al eliminar categoría');
      }
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingId(null);
    setFormData({ nombre: '', descripcion: '' });
  };

  if (loading) {
    return (
      <div className="loading-container">
        <motion.div
          className="loading-spinner"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
        <p>Cargando categorías...</p>
      </div>
    );
  }

  return (
    <div className="categorias-page">
      <div className="page-header">
        <motion.h1
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="page-icon">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9.568 3H5.25A2.25 2.25 0 003 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 005.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 009.568 3z" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 6h.008v.008H6V6z" />
          </svg>
          Categorías
        </motion.h1>
        <Button onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : '+ Nueva Categoría'}
        </Button>
      </div>

      {showForm && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card className="form-card">
            <h2>{editingId ? 'Editar Categoría' : 'Nueva Categoría'}</h2>
            <form onSubmit={handleSubmit}>
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
                <label>Descripción</label>
                <textarea
                  value={formData.descripcion}
                  onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
                  rows="3"
                />
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

      <motion.div className="categorias-grid" initial="hidden" animate="visible" variants={{ hidden: { opacity: 0 }, visible: { opacity: 1, transition: { staggerChildren: motionTokens.stagger } } }}>
        {categorias.map((categoria, index) => (
          <motion.div
            key={categoria.id}
            initial={{ x: 24, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: motionTokens.durationBase, ease: motionTokens.ease, delay: index * motionTokens.stagger }}
          >
            <Card>
              <div className="categoria-card">
                <h3>{categoria.nombre}</h3>
                <p>{categoria.descripcion || 'Sin descripción'}</p>
                <div className="card-actions">
                  <Button 
                    variant="outline" 
                    size="small"
                    onClick={() => handleEdit(categoria)}
                  >
                    Editar
                  </Button>
                  <Button 
                    variant="danger" 
                    size="small"
                    onClick={() => handleDelete(categoria.id)}
                  >
                    Eliminar
                  </Button>
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </motion.div>

      {categorias.length === 0 && !showForm && (
        <motion.div
          className="empty-state"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <h2>No hay categorías registradas</h2>
          <p>Comienza agregando tu primera categoría</p>
          <Button onClick={() => setShowForm(true)}>
            + Crear Categoría
          </Button>
        </motion.div>
      )}
    </div>
  );
};

export default CategoriasList;
