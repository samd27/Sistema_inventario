import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/dashboard/Dashboard';
import ProductosList from './pages/productos/ProductosList';
import CategoriasList from './pages/categorias/CategoriasList';
import ProveedoresList from './pages/proveedores/ProveedoresList';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/productos" element={<ProductosList />} />
            <Route path="/categorias" element={<CategoriasList />} />
            <Route path="/proveedores" element={<ProveedoresList />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
