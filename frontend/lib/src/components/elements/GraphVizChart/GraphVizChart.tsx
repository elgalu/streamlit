/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React, { ReactElement, useEffect } from "react"
import { select } from "d3"
import { graphviz } from "d3-graphviz"
import { logError } from "@streamlit/lib/src/util/log"
import withFullScreenWrapper from "@streamlit/lib/src/hocs/withFullScreenWrapper"
import { GraphVizChart as GraphVizChartProto } from "@streamlit/lib/src/proto"
import { StyledGraphVizChart } from "./styled-components"

export interface GraphVizChartProps {
  width: number
  element: GraphVizChartProto
  height?: number
}

interface Dimensions {
  chartWidth: number
  chartHeight: number
}

// Use d3Graphviz in a dummy expression so the library actually gets loaded.
// This way it registers itself in d3 as a plugin at this point.
const dummyGraphviz = graphviz
dummyGraphviz // eslint-disable-line @typescript-eslint/no-unused-expressions

const isFullScreen = (height = 0): boolean => Boolean(height)

export function GraphVizChart({
  width: propWidth,
  element,
  height: propHeight,
}: GraphVizChartProps): ReactElement {
  const chartId = `graphviz-chart-${element.elementId}`
  const isFull = isFullScreen(propHeight)

  let originalHeight = 0
  let originalWidth = 0

  const getChartDimensions = (): Dimensions => {
    const chartWidth = isFull
      ? propWidth
      : element.useContainerWidth
      ? propWidth
      : originalWidth
    const chartHeight = isFull ? propHeight || originalHeight : originalHeight
    return { chartWidth, chartHeight }
  }

  const setSvgDimensions = (node: SVGGraphicsElement): void => {
    originalHeight = Math.round(node.getBBox().height)
    originalWidth = Math.round(node.getBBox().width)

    select(node)
      .attr("width", isFull ? `${originalWidth}pt` : "100%")
      .attr("height", isFull ? `${originalHeight}pt` : "100%")
  }

  useEffect(() => {
    try {
      // Layout and render the graph
      const graph = graphviz(`#${chartId}`).zoom(false).fit(true).scale(1)

      graph.renderDot(element.spec).on("end", () => {
        const node = select(`#${chartId} > svg`).node()
        setSvgDimensions(node as SVGGraphicsElement)
      })
    } catch (error) {
      logError(error)
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [propWidth, element.spec])

  const elementDimensions = getChartDimensions()
  const width: number = elementDimensions.chartWidth || propWidth
  const height: number | undefined =
    elementDimensions.chartHeight || propHeight

  return (
    <StyledGraphVizChart
      className="graphviz stGraphVizChart"
      id={chartId}
      style={{ width, height }}
    />
  )
}

export default withFullScreenWrapper(GraphVizChart)