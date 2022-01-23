import React, { useState, useEffect } from "react";
import useFetch from "../hooks/useFetch";
import * as constantes from "../Constantes";

const Tabla = () => {
  const [paginaActual, setPaginaActual] = useState(1);

  const { loading, data } = useFetch(`${constantes.ObtenerCarDetectionRegistration}?offset=${5 * (paginaActual - 1)}`);
  const { data: dataPaginado } = useFetch(`${constantes.ObtenerCarDetectionRegistrationPaginado}`);

  const [registro, setRegistro] = useState([]);

  useEffect(() => {
    setRegistro(data);
  }, [data]);

  const handleSetPaginado = (numero) => {
    setPaginaActual(numero);
  };

  const handleSetPaginadoIncrementar = () => {
    if (paginaActual < dataPaginado) {
      setPaginaActual(paginaActual + 1);
    }
  };

  const handleSetPaginadoDecrementar = () => {
    if (paginaActual != 1) {
      setPaginaActual(paginaActual - 1);
    }
  };

  return (
    <>
      {loading ? (
        <div className="alert alert-info text-center">Cargando...</div>
      ) : (
        <div className="animate__animated animate__fadeIn">
          <table className="table table-hover">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Fecha</th>
                <th scope="col">Placa</th>
                <th scope="col">Frame</th>
                <th scope="col">Foto Placa</th>
              </tr>
            </thead>
            <tbody>
              {registro &&
                registro.map((element) => {
                  return (
                    <tr key={element[0]}>
                      <th scope="row">{element[0]}</th>
                      <td>{element[1]}</td>
                      <td>{element[2]}</td>
                      <td>{<img src={`${constantes.servidor_fotos_bdd}${element[3]}`} alt="Frame" width={500} />}</td>
                      <td>{<img src={`${constantes.servidor_fotos_bordes}${element[4]}`} alt="Foto Placa" width={400} />}</td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
          <nav aria-label="Page navigation example">
            <ul className="pagination">
              <li className="page-item">
                <a className="page-link" href="#" onClick={() => handleSetPaginadoDecrementar()}>
                  Anterior
                </a>
              </li>
              {dataPaginado &&
                Array.from(Array(dataPaginado).keys()).map((element) => {
                  return (
                    <li className="page-item" key={element} onClick={() => handleSetPaginado(element + 1)}>
                      <a className="page-link" href="#">
                        {element + 1}
                      </a>
                    </li>
                  );
                })}
              <li class="page-item">
                <a className="page-link" href="#" onClick={() => handleSetPaginadoIncrementar()}>
                  Siguiente
                </a>
              </li>
            </ul>
          </nav>
        </div>
      )}
    </>
  );
};

export default Tabla;
