import React, { useEffect, useState } from "react";
import { Avatar, List, message } from "antd";
import VirtualList from "rc-virtual-list";
import { IDocument } from "../Interfaces/document.interface";
import { BookOutlined } from "@ant-design/icons";

interface ListComponentProps {
  documents: IDocument[];
}
const ContainerHeight = 400;

const ListComponent: React.FC<ListComponentProps> = ({ documents }) => {

  return (
    <List>
      <VirtualList
        data={documents}
        height={ContainerHeight}
        itemHeight={47}
        itemKey="title"
        // onScroll={onScroll} //
      >
        {(item: IDocument) => (
          <List.Item key={item.title}>
            <List.Item.Meta
              avatar={<BookOutlined style={{ fontSize: "24px" }} />} // Usan
              title={<a href="https://ant.design">{item.title}</a>}
            />
          </List.Item>
        )}
      </VirtualList>
    </List>
  );
};

export default ListComponent;
