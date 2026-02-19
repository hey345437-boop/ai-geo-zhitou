import { Routes, Route } from 'react-router-dom';
import Layout from '@components/layout/Layout';
import Dashboard from '@pages/Dashboard';
import VisibilityResearch from '@pages/VisibilityResearch';
import EntityGraph from '@pages/EntityGraph';
import EvaluationProtocol from '@pages/EvaluationProtocol';
import BusinessImpact from '@pages/BusinessImpact';
import IntegrationHub from '@pages/IntegrationHub';
import StoreManagement from '@pages/StoreManagement';
import GeoAnalysis from '@pages/GeoAnalysis';
import DomainBenchmark from '@pages/DomainBenchmark';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="research" element={<VisibilityResearch />} />
        <Route path="entity-graph" element={<EntityGraph />} />
        <Route path="evaluation" element={<EvaluationProtocol />} />
        <Route path="business-impact" element={<BusinessImpact />} />
        <Route path="integrations" element={<IntegrationHub />} />
        <Route path="stores" element={<StoreManagement />} />
        <Route path="geo-analysis" element={<GeoAnalysis />} />
        <Route path="benchmark" element={<DomainBenchmark />} />
      </Route>
    </Routes>
  );
}

export default App;
