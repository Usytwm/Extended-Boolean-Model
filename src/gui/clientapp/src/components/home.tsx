import React, { useEffect, useState } from "react";
import ChartComponent from "./ChartComponent";
import AreaComponent from "./AreaChartComponent";
import { IData, IMetrics } from "../Interfaces/metrics.interface";
import { Card, Empty, Select, Spin } from "antd";
import ListComponent from "./listComponent";
import styles from "./styles.module.css";
import { IQuery } from "../Interfaces/query.interface";
import {
  getAllQueries,
  getMetrics,
  searchQuery,
  searchStandarQuery,
} from "../api/ApiService";
import { IDocument } from "../Interfaces/document.interface";

const HomeComponent = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const [isLoadingdocs, setIsLoadingdocs] = useState<boolean>(false);

  const [dataQuery, setdataQuery] = useState<IQuery[]>([]);

  const [document, setDocument] = useState<IDocument[]>([]);

  const [documentstarndar, setDocumentstarndar] = useState<IDocument[]>([]);

  const [metrics, setMetrics] = useState<IMetrics>();

  const [selectedQuery, setSelectedQuery] = useState<string | null>(null);

  useEffect(() => {
    const loadDocumentsAndMetrics = async () => {
      if (!selectedQuery) return;
      setIsLoadingdocs(true);
      try {
        const documents = await searchQuery(selectedQuery);
        setDocument(documents);

        const documentsstandar = await searchStandarQuery(selectedQuery);
        setDocumentstarndar(documentsstandar);

        const metricas = await getMetrics();
        setMetrics(metricas);
      } catch (error) {
        console.error("Error al cargar documentos o métricas", error);
      } finally {
        setIsLoadingdocs(false);
      }
    };

    loadDocumentsAndMetrics();
  }, [selectedQuery]);

  const loadDataQuery = async () => {
    if (dataQuery.length === 0) {
      try {
        setIsLoading(true);
        const recivedQueryes = await getAllQueries();
        setdataQuery(recivedQueryes);
      } catch (error) {
        console.error("Error al cargar datos", error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const onDropdownVisibleChange = (isVisible: boolean) => {
    if (isVisible) {
      loadDataQuery();
    }
  };

  const onQueryChange = (value: string) => {
    setSelectedQuery(value);
    console.log(value);
  };

  return (
    <div className={`${styles.homecontainer}`}>
      <div className={`${styles.leftpanel}`}>
        <Card style={{ width: "auto" }} className={styles.card}>
          <Select
            className={styles.select}
            showSearch
            placeholder="Selecciona una opción"
            optionFilterProp="children"
            onDropdownVisibleChange={onDropdownVisibleChange}
            notFoundContent={
              isLoading ? (
                <Spin
                  tip="Cargando..."
                  style={{
                    width: "100%",
                    display: "flex",
                    justifyContent: "center",
                  }}
                />
              ) : null
            }
            onChange={onQueryChange}
            style={{ width: 500, height: 50 }}
            options={dataQuery.map((dato) => ({
              value: dato?.id?.toString() + "," + dato?.name,
              label: dato?.name,
            }))}
          />
          <h2>Extended Boolean Model</h2>
          {isLoadingdocs ? (
            <Spin
              style={{
                width: "100%",
                display: "flex",
                justifyContent: "center",
              }}
            />
          ) : document.length > 0 ? (
            <Card style={{ width: "auto" }}>
              <ListComponent documents={document} />
            </Card>
          ) : (
            <div className={`${styles.cardContentCentered}`}>
              <Empty description="No se encontraron documentos" />
            </div>
          )}
          <h2>Standar Boolean Model</h2>
          {isLoadingdocs ? (
            <Spin
              style={{
                width: "100%",
                display: "flex",
                justifyContent: "center",
              }}
            />
          ) : documentstarndar.length > 0 ? (
            <Card style={{ width: "auto" }}>
              <ListComponent documents={documentstarndar} />
            </Card>
          ) : (
            <div className={`${styles.cardContentCentered}`}>
              <Empty description="No se encontraron documentos" />
            </div>
          )}
        </Card>
      </div>
      <div className={`${styles.rightpanel}`}>
        <Card
          style={{ width: "auto" }}
          className={`${styles.card}  ${styles.cardContentCentered}`}
        >
          {isLoadingdocs ? (
            <Spin
              style={{
                width: "100%",
                display: "flex",
                justifyContent: "center",
              }}
            />
          ) : metrics ? (
            <>
              <ChartComponent data={metrics?.data} />
              <AreaComponent data={metrics?.data} />
            </>
          ) : (
            <Empty description="No se encontraron métricas" />
          )}
        </Card>
      </div>
    </div>
  );
};

export default HomeComponent;
