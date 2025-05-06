import { useParams } from "react-router-dom";

function DBInfo() {
    const id = useParams().id;
    const properties = [
        { name: "UUID", value: id },
        { name: "Database Name", value: "SampleDB" },
        { name: "Database Size", value: "20GB" },
        { name: "Created At", value: "2023-01-01" },
        { name: "Last Updated", value: "2023-10-01" },
        { name: "number of Tables", value: "5" },
        { name: "Quota Usage / Week", value: "1 Unit"}
    ]
    return (
        <>
            <table className="rounded table table-striped table-bordered border-colapse border border-gray-400">
                
                <tbody className="text-center rounded">
{properties.map((property, index) => (
                    <tr key={index}>
                        <td className="border border-gray-400 p-1">{property.name}</td>
                        <td className="border border-gray-400 p-1">{property.value}</td>
                    </tr>))}
                </tbody>
            </table>
        </>
    );
}

export default DBInfo;