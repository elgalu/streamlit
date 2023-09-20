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

import React from "react"
import "@testing-library/jest-dom"
import { screen } from "@testing-library/react"

import { DocString as DocStringProto } from "@streamlit/lib/src/proto"
import DocString, { DocStringProps, Member } from "./DocString"
import { render } from "@streamlit/lib/src/test_util"

const getProps = (
  elementProps: Partial<DocStringProto> = {}
): DocStringProps => ({
  element: DocStringProto.create({
    name: "st.balloons",
    value: "streamlit.balloons()",
    docString: "docstring",
    type: "method",
    ...elementProps,
  }),
  width: 0,
})

describe("DocString Element", () => {
  const props = getProps()

  it("renders without crashing", () => {
    render(<DocString {...props} />)
    expect(screen.getAllByTestId("stDocstring")).toHaveLength(2)
  })

  it("should render a doc-string", () => {
    render(<DocString {...props} />)
    expect(screen.getByText(props.element.docString)).toBeInTheDocument()
    expect(screen.getByTestId("stDocstringDocstring")).toBeInTheDocument()
  })

  it("should render 'no docs' text when empty", () => {
    const props = getProps({
      docString: undefined,
    })
    render(<DocString {...props} />)
    expect(screen.getAllByTestId("stDocstring")).toHaveLength(1)
    expect(screen.getByTestId("stDocstringDocstring")).toBeInTheDocument()
    expect(screen.getByText("No docs available")).toBeInTheDocument()
  })

  describe("doc-header", () => {
    it("should render a name", () => {
      render(<DocString {...props} />)
      expect(screen.getByTestId("stDocstringDocName")).toBeInTheDocument()
      expect(screen.getByText("st.balloons")).toBeInTheDocument()
    })

    it("should render value", () => {
      render(<DocString {...props} />)
      expect(screen.getByTestId("stDocstringDocValue")).toBeInTheDocument()
      expect(screen.getByText("streamlit.balloons()")).toBeInTheDocument()
    })

    it("should render a type", () => {
      render(<DocString {...props} />)
      expect(screen.getByTestId("stDocstringDocType")).toBeInTheDocument()
      expect(screen.getByText("method")).toBeInTheDocument()
    })

    describe("should render empty when", () => {
      const props = getProps({
        name: undefined,
        value: undefined,
        type: undefined,
      })
      render(<DocString {...props} />)

      it("there's no name", () => {
        expect(screen.queryByTestId("stDocstring")).not.toBeInTheDocument()
        expect(
          screen.queryByTestId("stDocstringDocName")
        ).not.toBeInTheDocument()
      })

      it("there's no value", () => {
        expect(screen.queryByTestId("stDocstring")).not.toBeInTheDocument()
        expect(
          screen.queryByTestId("stDocstringDocValue")
        ).not.toBeInTheDocument()
      })

      it("there's no type", () => {
        expect(screen.queryByTestId("stDocstring")).not.toBeInTheDocument()
        expect(
          screen.queryByTestId("stDocstringDocType")
        ).not.toBeInTheDocument()
      })
    })

    // Testing cases that we expect to happen (won't test every combination)
    it("should render a type and value when there's no name", () => {
      const props = getProps({
        name: undefined,
      })
      render(<DocString {...props} />)

      expect(
        screen.queryByTestId("stDocstringDocName")
      ).not.toBeInTheDocument()

      expect(screen.getByTestId("stDocstringDocType")).toBeInTheDocument()
      expect(screen.getByText("method")).toBeInTheDocument()

      expect(screen.getByTestId("stDocstringDocValue")).toBeInTheDocument()
      expect(screen.getByText("streamlit.balloons()")).toBeInTheDocument()
    })

    // Testing cases that we expect to happen (won't test every combination)
    it("should render a name and type when there's no value", () => {
      const props = getProps({
        value: undefined,
      })
      render(<DocString {...props} />)

      expect(
        screen.queryByTestId("stDocstringDocValue")
      ).not.toBeInTheDocument()

      expect(screen.getByTestId("stDocstringDocName")).toBeInTheDocument()
      expect(screen.getByText("st.balloons")).toBeInTheDocument()

      expect(screen.getByTestId("stDocstringDocType")).toBeInTheDocument()
      expect(screen.getByText("method")).toBeInTheDocument()
    })
  })

  describe("members table", () => {
    it("should render no members when there are none", () => {
      render(<DocString {...props} />)
      expect(
        screen.queryByTestId("stDocstringMembersTable")
      ).not.toBeInTheDocument()
    })

    it("should render members", () => {
      const props = getProps({
        members: [
          {
            name: "member1",
            value: "value1",
            type: "type1",
          },
          {
            name: "member2",
            value: "value2",
            type: "type2",
          },
        ],
      })
      render(<DocString {...props} />)

      expect(screen.getByTestId("stDocstringMembersTable")).toBeInTheDocument()
      expect(screen.getAllByTestId("stMember")).toHaveLength(2)
    })
  })
})

describe("Member Element", () => {
  it("should render value-oriented members", () => {
    const props = {
      member: {
        name: "member1",
        type: "type1",
        value: "value1",
      },
    }

    render(<Member {...props} />)

    expect(screen.getByTestId("stMemberDocValue")).toBeInTheDocument()
    expect(screen.getByText("value1")).toBeInTheDocument()

    expect(screen.getByTestId("stMemberDocName")).toBeInTheDocument()
    expect(screen.getByText("member1")).toBeInTheDocument()

    expect(screen.getByTestId("stMemberDocType")).toBeInTheDocument()
    expect(screen.getByText("type1")).toBeInTheDocument()
  })

  it("should render doc-oriented members", () => {
    const props = {
      member: {
        name: "member1",
        type: "type1",
        docString: "docstring1",
      },
    }

    render(<Member {...props} />)

    expect(screen.getByTestId("stMemberDocName")).toBeInTheDocument()
    expect(screen.getByText("member1")).toBeInTheDocument()

    expect(screen.getByTestId("stMemberDocType")).toBeInTheDocument()
    expect(screen.getByText("type1")).toBeInTheDocument()

    expect(screen.getByTestId("stMemberDocString")).toBeInTheDocument()
    expect(screen.getByText("docstring1")).toBeInTheDocument()
  })

  it("should prefer value over doc", () => {
    const props = {
      member: {
        name: "member1",
        type: "type1",
        value: "value1",
        docString: "docstring1",
      },
    }

    render(<Member {...props} />)

    expect(screen.getByTestId("stMemberDocValue")).toBeInTheDocument()
    expect(screen.getByText("value1")).toBeInTheDocument()

    expect(screen.getByTestId("stMemberDocName")).toBeInTheDocument()
    expect(screen.getByText("member1")).toBeInTheDocument()

    expect(screen.getByTestId("stMemberDocType")).toBeInTheDocument()
    expect(screen.getByText("type1")).toBeInTheDocument()

    expect(screen.queryByTestId("stMemberDocString")).not.toBeInTheDocument()
    expect(screen.queryByText("docstring1")).not.toBeInTheDocument()
  })

  it("should tell you when there are no docs", () => {
    const props = {
      member: {
        name: "member1",
        type: "type1",
      },
    }

    render(<Member {...props} />)

    expect(screen.getByTestId("stMemberDocString")).toBeInTheDocument()
    expect(screen.getByText("No docs available")).toBeInTheDocument()
  })

  it("should only show type if present", () => {
    const props = {
      member: {
        name: "member1",
      },
    }

    render(<Member {...props} />)

    expect(screen.queryByTestId("stMemberDocType")).not.toBeInTheDocument()
  })
})
