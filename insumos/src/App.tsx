import { Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout"
import Home from "./Home";
import ProductoList from "./pages/ProductoList";
import CategoriaList from "./pages/CategoriaList";

export default function App() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/productos" element={<ProductoList />} />
        <Route path="/categorias" element={<CategoriaList />} />
      </Routes>
    </MainLayout>
  );
}
