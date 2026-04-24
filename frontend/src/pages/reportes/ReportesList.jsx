import { useEffect, useState } from 'react';
import Card from '../../components/Card';
import Button from '../../components/Button';
import { reportesAPI } from '../../services/api';
import './ReportesList.css';

const ReportesList = () => {
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [resumen, setResumen] = useState(null);
  const [tendencia, setTendencia] = useState([]);

  const fetchReportes = async () => {
    try {
      setLoading(true);
      setError('');
      const [resumenRes, tendenciaRes] = await Promise.all([
        reportesAPI.getResumen(),
        reportesAPI.getTendenciaBajoStock(),
      ]);
      setResumen(resumenRes.data.data || null);
      setTendencia(tendenciaRes.data.data || []);
    } catch (err) {
      setError(err?.response?.data?.error || 'No fue posible cargar reportes');
    } finally {
      setLoading(false);
    }
  };

  const generarSnapshot = async () => {
    try {
      setGenerating(true);
      setError('');
      await reportesAPI.generarSnapshotBajoStock();
      await fetchReportes();
    } catch (err) {
      setError(err?.response?.data?.error || 'No fue posible generar snapshot');
    } finally {
      setGenerating(false);
    }
  };

  useEffect(() => {
    fetchReportes();
  }, []);

  return (
    <div className="reportes-page">
      <div className="reportes-header">
        <h1>Reportes y Analitica</h1>
        <p>Resumen ejecutivo, snapshots y tendencia histórica de bajo stock.</p>
      </div>

      <div className="reportes-actions">
        <Button variant="success" onClick={generarSnapshot} disabled={generating}>
          {generating ? 'Generando...' : 'Generar snapshot bajo stock'}
        </Button>
        <Button variant="outline" onClick={fetchReportes} disabled={loading}>
          Recargar
        </Button>
      </div>

      {error && (
        <Card className="error-card">
          <p>{error}</p>
        </Card>
      )}

      {loading ? (
        <Card>
          <p>Cargando reportes...</p>
        </Card>
      ) : (
        <>
          <div className="kpi-grid">
            <Card><h3>Total Productos</h3><p>{resumen?.total_productos ?? 0}</p></Card>
            <Card><h3>Total Categorias</h3><p>{resumen?.total_categorias ?? 0}</p></Card>
            <Card><h3>Total Proveedores</h3><p>{resumen?.total_proveedores ?? 0}</p></Card>
            <Card><h3>Productos Bajo Stock</h3><p>{resumen?.productos_bajo_stock ?? 0}</p></Card>
            <Card><h3>Stock Total Unidades</h3><p>{resumen?.stock_total_unidades ?? 0}</p></Card>
            <Card><h3>Valor Total Estimado</h3><p>${resumen?.valor_total_estimado ?? 0}</p></Card>
          </div>

          <Card>
            <h3>Tendencia de Bajo Stock</h3>
            {tendencia.length === 0 ? (
              <p>No hay datos de tendencia. Genera un snapshot para comenzar.</p>
            ) : (
              <div className="tendencia-list">
                {tendencia.map((item) => (
                  <div key={item.fecha} className="tendencia-item">
                    <span>{item.fecha}</span>
                    <strong>{item.total_bajo_stock}</strong>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </>
      )}
    </div>
  );
};

export default ReportesList;
