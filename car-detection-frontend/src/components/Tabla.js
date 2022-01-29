import React, { useState, useEffect } from "react";
import useFetch from "../hooks/useFetch";
import * as constantes from "../Constantes";
import DateTimePicker from "@mui/lab/DateTimePicker";
import TextField from "@mui/material/TextField";

import AdapterDateFns from "@mui/lab/AdapterDateFns";
import LocalizationProvider from "@mui/lab/LocalizationProvider";

const Tabla = () => {
  const [valueHasta, setValueHasta] = React.useState(new Date(Date.now()));

  const handleChangeHasta = (newValue) => {
    setValueHasta(newValue);
  };
  var dt = new Date(Date.now());
  dt.setDate(dt.getDate() - 10);

  const [valueDesde, setValueDesde] = React.useState(dt);

  const handleChangeDesde = (newValue) => {
    setValueDesde(newValue);
  };

  const [paginaActual, setPaginaActual] = useState(1);

  const { loading, data } = useFetch(`${constantes.ObtenerCarDetectionRegistration}?offset=${5 * (paginaActual - 1)}&desde=${valueDesde.toISOString()}&hasta=${valueHasta.toISOString()}`);
  const { data: dataPaginado } = useFetch(`${constantes.ObtenerCarDetectionRegistrationPaginado}?desde=${valueDesde.toISOString()}&hasta=${valueHasta.toISOString()}`);

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
    if (paginaActual !== 1) {
      setPaginaActual(paginaActual - 1);
    }
  };

  return (
    <>
      {loading ? (
        <div className="alert alert-info text-center">Cargando...</div>
      ) : (
        <div className="animate__animated animate__fadeIn">
          <div className="row mb-5 mt-5">
            <div className="col text-center">
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DateTimePicker label="Desde" value={valueDesde} onChange={handleChangeDesde} renderInput={(params) => <TextField {...params} />} />
              </LocalizationProvider>
            </div>
            <div className="col text-center">
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DateTimePicker label="Hasta" value={valueHasta} onChange={handleChangeHasta} renderInput={(params) => <TextField {...params} />} />
              </LocalizationProvider>
            </div>
          </div>

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

          {dataPaginado && dataPaginado !== 0 ? (
            <nav aria-label="Page navigation example">
              <ul className="pagination">
                <li className="page-item">
                  <a className="page-link" href="#" onClick={() => handleSetPaginadoDecrementar()}>
                    Anterior
                  </a>
                </li>
                {Array.from(Array(dataPaginado).keys()).map((element) => {
                  return (
                    <li className="page-item" key={element} onClick={() => handleSetPaginado(element + 1)}>
                      <a className="page-link" href="#">
                        {element + 1}
                      </a>
                    </li>
                  );
                })}
                <li className="page-item">
                  <a className="page-link" href="#" onClick={() => handleSetPaginadoIncrementar()}>
                    Siguiente
                  </a>
                </li>
              </ul>
            </nav>
          ) : (
            <h2>No se encontró ningún registro.</h2>
          )}
        </div>
      )}
    </>
  );
};

export default Tabla;
